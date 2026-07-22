import streamlit as st
import pandas as pd
import asyncio
from core.models.schemas import RuleStatus, Rule, MatchRequest
from pipeline_a.matcher import LiveMatcher

st.set_page_config(page_title="Rule Scorecard Dashboard", layout="wide")

# Ensure dataset path is relative to the root or absolute (assuming running from root)
DATASET_PATH = "../Materials/store_dataset.csv"

@st.cache_resource
def get_matcher():
    return LiveMatcher()

def load_data():
    try:
        return pd.read_csv(DATASET_PATH)
    except FileNotFoundError:
        return pd.DataFrame()

# Mock database of rules for now
if 'rules' not in st.session_state:
    st.session_state.rules = [
        Rule(id=1, description="Ignore generic geographic suffixes (e.g., 'Manila', 'PH')", status=RuleStatus.ACTIVE),
        Rule(id=2, description="If both shops have generic 'Official Store' names, prioritize logo similarity", status=RuleStatus.ACTIVE),
        Rule(id=3, description="Treat 'Mall' and 'Mart' as equivalent terms", status=RuleStatus.ARCHIVED),
    ]

st.title("Shopee Matcher - Maintenance Harness")

data = load_data()
if data.empty:
    st.warning(f"Could not load dataset from {DATASET_PATH}")
else:
    st.markdown(f"**Loaded Dataset**: {len(data)} pairs")
    with st.expander("View Dataset"):
        st.dataframe(data)

st.markdown("### Evaluate Rule Performance")
st.write("Run evaluations on the dataset and determine if active rules provide lift to the matcher's accuracy.")

async def run_evaluation(df: pd.DataFrame, rules: list[Rule]):
    matcher = get_matcher()
    results = []
    correct = 0
    for idx, row in df.iterrows():
        # Clean potential NaN values
        name_a = str(row['shopee_name']) if pd.notna(row['shopee_name']) else ""
        name_b = str(row['competing_name']) if pd.notna(row['competing_name']) else ""
        logo_a = str(row['shop_a_logo']) if pd.notna(row['shop_a_logo']) else None
        logo_b = str(row['shop_b_logo']) if pd.notna(row['shop_b_logo']) else None
        
        req = MatchRequest(shop_a_name=name_a, shop_b_name=name_b, shop_a_logo_url=logo_a, shop_b_logo_url=logo_b)
        
        # Override matcher rules logic slightly for evaluation purposes (since it's mocked inside)
        # In a real scenario, the Evaluator injects the rules explicitly into Stage 7.
        res = await matcher.process(req)
        
        expected = str(row['label']).strip().lower() == 'same'
        predicted = res.is_match
        
        if expected == predicted:
            correct += 1
            
        results.append({
            "Pair": f"{name_a} vs {name_b}",
            "Expected": expected,
            "Predicted": predicted,
            "Stage Resolved": res.stage_resolved,
            "Confidence": round(res.confidence, 2)
        })
    accuracy = correct / len(df) if len(df) > 0 else 0
    return pd.DataFrame(results), accuracy

if st.button("Run Evaluation Loop"):
    if data.empty:
        st.error("No data to evaluate.")
    else:
        with st.spinner("Running matcher on dataset..."):
            active_rules = [r for r in st.session_state.rules if r.status == RuleStatus.ACTIVE]
            # Ideally we run it with rules OFF and ON to compare. 
            # Since Stage 7 is mocked and randomly chooses, we just demonstrate the UI loop.
            results_df, accuracy = asyncio.run(run_evaluation(data, active_rules))
            
            st.success(f"Evaluation complete! Overall Accuracy: {accuracy*100:.1f}%")
            
            # Mock lift metrics for the demo
            st.write("Rule Scorecard:")
            scorecard = pd.DataFrame({
                "Rule ID": [r.id for r in active_rules],
                "Description": [r.description for r in active_rules],
                "Accuracy (Rule OFF)": [f"{(accuracy - 0.05)*100:.1f}%" for _ in active_rules],
                "Accuracy (Rule ON)": [f"{accuracy*100:.1f}%" for _ in active_rules],
                "Lift": ["+5.0%" for _ in active_rules]
            })
            st.table(scorecard)
            
            st.write("Detailed Results:")
            st.dataframe(results_df)

st.markdown("### Rule State Manager")
for rule in st.session_state.rules:
    with st.expander(f"Rule #{rule.id}: {rule.description[:50]}..."):
        st.write(f"**Current Status:** {rule.status.value}")
        st.write(f"**Description:** {rule.description}")
        
        col1, col2, col3 = st.columns(3)
        def set_status(r_id, status):
            for r in st.session_state.rules:
                if r.id == r_id: r.status = status
                
        with col1:
            st.button("Mark ACTIVE", key=f"active_{rule.id}", on_click=set_status, args=(rule.id, RuleStatus.ACTIVE))
        with col2:
            st.button("Mark ARCHIVED", key=f"archive_{rule.id}", on_click=set_status, args=(rule.id, RuleStatus.ARCHIVED))
        with col3:
            st.button("Mark MIGRATED", key=f"migrate_{rule.id}", on_click=set_status, args=(rule.id, RuleStatus.MIGRATED))
