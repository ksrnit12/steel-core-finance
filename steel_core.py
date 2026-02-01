import pandas as pd
import sys
from pathlib import Path
from audit_core import AuditLogger

class ArchitectAgent:
    def __init__(self):
        # Setup paths
        self.base_path = Path(__file__).parent
        self.data_path = self.base_path / 'finance_data.csv'
        self.log_path = self.base_path / 'steel_core_audit.jsonl'
        
        self.auditor = AuditLogger(log_file=str(self.log_path))
        
        if self.data_path.exists():
            self.data = pd.read_csv(self.data_path)
            # Clean currency columns just in case
            for col in ['Revenue', 'Cost']:
                if self.data[col].dtype == 'O':
                    self.data[col] = self.data[col].replace('[\$,]', '', regex=True).astype(float)
            print(f'✅ System Online. Linked to {self.data_path.name}')
        else:
            print(f'❌ Error: Could not find {self.data_path.name}')
            sys.exit(1)

    def process_query(self, user_prompt: str):
        prompt_lower = user_prompt.lower()

        # --- THE ROUTER (Brain) ---
        if 'profit' in prompt_lower:
            return self._calculate_profit()
        elif 'project' in prompt_lower:
            # Extract project name logic
            return self._lookup_project(prompt_lower)
        else:
            return 'I can only handle auditable profit or project queries.'

    def _calculate_profit(self):
        revenue = self.data['Revenue'].sum()
        cost = self.data['Cost'].sum()
        profit = revenue - cost

        audit_id = self.auditor.log_event(
            action_type='CALC_PROFIT',
            inputs={'revenue': float(revenue), 'cost': float(cost)},
            result=float(profit),
            source=self.data_path.name
        )
        return f'Total Profit: ${profit:,.2f} (Audit ID: {audit_id})'

    def _lookup_project(self, prompt):
        # Find which project the user is talking about
        found_row = None
        for name in self.data['Project']:
            if name.lower().replace('_', ' ') in prompt.replace('_', ' '):
                found_row = self.data[self.data['Project'] == name].iloc[0]
                break
        
        if found_row is None:
            return "Project not found in secure vault."

        # Log the Lookup
        audit_id = self.auditor.log_event(
            action_type='LOOKUP_PROJECT',
            inputs={'search_term': prompt},
            result={'status': found_row['Status'], 'revenue': float(found_row['Revenue'])},
            source=self.data_path.name
        )
        
        return f"📊 {found_row['Project']}: Status is {found_row['Status']}. Revenue is ${found_row['Revenue']:,.2f} (Audit ID: {audit_id})"

if __name__ == '__main__':
    agent = ArchitectAgent()
    print('\n--- DEMO MODE ---')
    print('User: How is Project Alpha doing?')
    print(f'AI: {agent.process_query("how is project alpha doing")}')
    
    print('\nUser: What is the total profit?')
    print(f'AI: {agent.process_query("what is the total profit")}')
