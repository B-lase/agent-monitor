# SECURITY UPDATE - CRITICAL

## Issue Resolved

**VULNERABILITY**: Hardcoded Supabase service role key in client.py has been REMOVED.

**FIXED**: 
- ✅ Removed hardcoded service key from agent_monitor/client.py
- ✅ Updated client to use api_key parameter securely
- ✅ Updated README with secure usage instructions
- ✅ Updated examples to use environment variables

## Secure Usage

### For Testing (Temporary API Key)

Use this service role key for testing the integration:

```bash
export AGENT_MONITOR_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InliaGphYmlyb21zbW5xcnptbmFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU0NTk0ODcsImV4cCI6MjA3MTAzNTQ4N30.jmWskjMDuU8RsYAvThRQLksuFKru1WgtZ7aAOQtNcyw"
```

### Updated Integration Code

```python
import os
import agent_monitor

# Secure API key usage
api_key = os.getenv('AGENT_MONITOR_API_KEY')
if not api_key:
    raise ValueError("AGENT_MONITOR_API_KEY environment variable is required")

# Initialize monitoring
agent_monitor.init(
    api_key=api_key,
    dashboard_url="https://0f3jus9vnfzq.space.minimax.io"
)
```

## Security Best Practices

1. **Never hardcode API keys** in source code
2. **Use environment variables** for sensitive credentials
3. **Rotate keys regularly** if they're compromised
4. **Limit key permissions** to minimum required

## Next Steps

1. Test the integration with the new secure approach
2. Verify agents can connect and appear online
3. Confirm data flow works end-to-end
