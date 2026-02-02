import pandas as pd
import sys
from pathlib import Path
# Imports your existing AuditLogger class
from audit_core import AuditLogger

class ArchitectAgent:
    def __init__(self):
        # Setup paths relative to this script
        self.base_path = Path(__file__).parent
        self.data_path = self.base_path / 'finance_data.csv'
        self.log_path = self.base_path / 'steel_core_audit.jsonl'
        
        # Initialize your existing auditor
        # We pass the path as a string to match your class definition
        self.auditor = AuditLogger(log_file=str(self.log_path))
        
        # --- DATA LOADING & SAFETY CHECKS ---
        if self.data_path.exists():
            self.data = pd.read_csv(self.data_path)
            # Clean currency columns (remove $ and ,) just in case
            for col in ['Revenue', 'Cost']:
                if col in self.data.columns and self.data[col].dtype == 'O':
                    self.data[col] = self.data[col].replace('[\$,]', '', regex=True).astype(float)
            print(f'✅ System Online. Linked to {self.data_path.name}')
        else:
            print(f'❌ Warning: Could not find {self.data_path.name}')
            print('⚠️  Auto-generating dummy financial data for demo...')
            # Create dummy data so the code never crashes for new users
            df = pd.DataFrame({
                'Project': ['Project_Alpha', 'Project_Beta', 'Project_Gamma'],
                'Status': ['Active', 'Planning', 'Closed'],
                'Revenue': [1000000.00, 500000.00, 750000.00],
                'Cost': [600000.00, 200000.00, 400000.00]
            })
            df.to_csv(self.data_path, index=False)
            self.data = df
            print(f'✅ Dummy data created at {self.data_path.name}')

    def process_query(self, user_prompt: str):
        """The Router: Decides if the query is safe for the Steel Core."""
        prompt_lower = user_prompt.lower()

        # --- THE ROUTER (Brain) ---
        if 'profit' in prompt_lower:
            return self._calculate_profit()
        elif 'project' in prompt_lower:
            return self._lookup_project(prompt_lower)
        else:
            return 'I can only handle auditable profit or project queries.'

    def _calculate_profit(self):
        """Deterministic Math: Python does the math, not the LLM."""
        revenue = self.data['Revenue'].sum()
        cost = self.data['Cost'].sum()
        profit = revenue - cost

        # Uses your log_event method
        audit_id = self.auditor.log_event(
            action_type='CALC_PROFIT',
            inputs={'revenue': float(revenue), 'cost': float(cost)},
            result=float(profit),
            source=self.data_path.name
        )
        return f'Total Profit: ${profit:,.2f} (Audit ID: {audit_id})'

    def _lookup_project(self, prompt):
        """Deterministic Lookup: Fetch exact records."""
        # Find which project the user is talking about
        found_row = None
        for name in self.data['Project']:
            # Flexible matching (handles "project alpha" vs "Project_Alpha")
            if name.lower().replace('_', ' ') in prompt.replace('_', ' '):
                found_row = self.data[self.data['Project'] == name].iloc[0]
                break
        
        if found_row is None:
            # Log the failure too for security
            self.auditor.log_event(
                action_type='LOOKUP_FAILED',
                inputs={'search_term': prompt},
                result='Not Found',
                source=self.data_path.name
            )
            return "❌ Project not found in secure vault."

        # Log the Success
        audit_id = self.auditor.log_event(
            action_type='LOOKUP_PROJECT',
            inputs={'search_term': prompt},
            result={'status': found_row['Status'], 'revenue': float(found_row['Revenue'])},
            source=self.data_path.name
        )
        
        # Return formatted string (The "Voice Layer")
        return (f"📊 {found_row['Project']}\n"
                f"   Status: {found_row['Status']}\n"
                f"   Revenue: ${found_row['Revenue']:,.2f}\n"
                f"   Cost: ${found_row['Cost']:,.2f}\n"
                f"   (Audit ID: {audit_id})")

# --- DEMO MODE (Runs when you execute the script) ---
if __name__ == '__main__':
    agent = ArchitectAgent()
    
    print('\n' + '='*60)
    print('STEEL CORE FINANCE ENGINE - DEMO')
    print('='*60)
    
    print('\n[Query 1] Project Lookup')
    print('-'*60)
    print('User: How is Project Alpha doing?')
    result1 = agent.process_query("how is project alpha doing")
    print(f'AI: {result1}')
    
    print('\n[Query 2] Profit Calculation')
    print('-'*60)
    print('User: What is the total profit?')
    result2 = agent.process_query("what is the total profit")
    print(f'AI: {result2}')
    
    print('\n' + '='*60)
    print(f'✅ All calculations logged to {agent.log_path.name}')
    print('='*60)
