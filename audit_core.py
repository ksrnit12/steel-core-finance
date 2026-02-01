import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AuditSystem')

class AuditLogger:
    def __init__(self, log_file: str = 'steel_core_audit.jsonl'):
        self.log_file = Path(log_file)
        self._initialize_log()
    
    def _initialize_log(self):
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                header = {'system': 'Steel Core', 'timestamp': datetime.utcnow().isoformat()}
                f.write(json.dumps(header) + '\n')
    
    def log_event(self, action_type: str, inputs: Dict[str, Any], result: Any, source: str) -> str:
        audit_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'action_type': action_type,
            'inputs': inputs,
            'result': result,
            'source': source
        }
        record_str = json.dumps(audit_record, sort_keys=True)
        audit_hash = hashlib.sha256(record_str.encode()).hexdigest()[:16]
        final_entry = {'audit_id': audit_hash, **audit_record}
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(final_entry) + '\n')
            return audit_hash
        except Exception as e:
            logger.error(f'Audit Write Failed: {e}')
            return 'AUDIT_FAILURE'
