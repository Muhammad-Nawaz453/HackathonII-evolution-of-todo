# k9s - Kubernetes Terminal UI (FREE)

k9s is a terminal-based UI for managing Kubernetes clusters. It's completely free, open source, and requires no API keys or paid services.

## Installation

### Windows (via Chocolatey)
```bash
choco install k9s
```

### Windows (via Scoop)
```bash
scoop install k9s
```

### macOS (via Homebrew)
```bash
brew install k9s
```

### Linux (via package manager)
```bash
# Ubuntu/Debian
sudo apt install k9s

# Arch Linux
sudo pacman -S k9s

# Or download binary from GitHub
curl -sS https://webinstall.dev/k9s | bash
```

## Quick Start

### Launch k9s
```bash
# Connect to current kubectl context
k9s

# Connect to specific context
k9s --context minikube

# Connect to specific namespace
k9s -n todo-app-dev
```

## Essential Keyboard Shortcuts

### Navigation
- `:` - Command mode (type resource name, e.g., `:pods`, `:svc`, `:deploy`)
- `/` - Filter/search current view
- `Esc` - Back/cancel
- `?` - Help (shows all shortcuts)
- `Ctrl+A` - Show all available resources

### Resource Management
- `d` - Describe selected resource
- `l` - View logs
- `e` - Edit resource (opens in editor)
- `y` - View YAML
- `Ctrl+D` - Delete resource
- `s` - Shell into pod

### View Controls
- `0` - Show all namespaces
- `1-9` - Show specific namespace
- `Ctrl+R` - Refresh
- `Ctrl+S` - Save current view
- `Ctrl+Z` - Toggle wide columns

### Logs
- `l` - View logs
- `p` - Previous logs (for crashed containers)
- `f` - Toggle follow mode
- `w` - Toggle wrap
- `t` - Toggle timestamps

## Common Workflows

### 1. Check Pod Status
```
1. Launch k9s
2. Type `:pods` (or just `:po`)
3. Navigate with arrow keys
4. Press `d` to describe a pod
5. Press `l` to view logs
```

### 2. Debug Failing Pod
```
1. k9s -n todo-app-dev
2. :pods
3. Find failing pod (red status)
4. Press `d` to see events
5. Press `l` to view logs
6. Press `s` to shell into pod (if running)
```

### 3. Scale Deployment
```
1. :deployments
2. Select deployment
3. Press `s` to scale
4. Enter desired replica count
```

### 4. View Service Endpoints
```
1. :services
2. Select service
3. Press `d` to describe
4. View endpoints and ports
```

### 5. Monitor Resource Usage
```
1. :pods
2. Press `Shift+F` to show resource usage
3. Sort by CPU or memory
```

## Configuration

k9s can be customized with a config file at `~/.k9s/config.yml`:

```yaml
k9s:
  # Refresh rate in seconds
  refreshRate: 2

  # Max number of logs lines
  maxConnRetry: 5

  # Enable mouse support
  enableMouse: true

  # Default namespace
  namespace:
    active: todo-app-dev
    favorites:
      - todo-app-dev
      - todo-app-prod
      - default

  # UI settings
  ui:
    enableMouse: true
    headless: false
    logoless: false
    crumbsless: false
    noIcons: false
```

## Aliases (Optional)

Add to your shell profile for quick access:

```bash
# ~/.bashrc or ~/.zshrc
alias k9='k9s'
alias k9d='k9s -n todo-app-dev'
alias k9p='k9s -n todo-app-prod'
```

## Advantages Over kubectl-ai and kagent

### k9s (FREE)
✅ No API keys required
✅ No internet connection needed
✅ No cost ($0/month)
✅ Fast and responsive
✅ Works offline
✅ Open source
✅ Active community
✅ No rate limits

### kubectl-ai (PAID)
❌ Requires OpenAI API key
❌ Costs money per request
❌ Requires internet
❌ Rate limits apply
❌ Slower (API calls)

### kagent (PAID)
❌ Requires OpenAI API key
❌ Costs money per request
❌ Requires internet
❌ Complex setup
❌ Rate limits apply

## Tips and Tricks

### 1. Quick Resource Access
Type `:` followed by resource abbreviation:
- `:po` - Pods
- `:svc` - Services
- `:deploy` - Deployments
- `:ing` - Ingresses
- `:cm` - ConfigMaps
- `:sec` - Secrets

### 2. Filter Resources
Press `/` and type filter:
- `/backend` - Show only resources with "backend"
- `/Running` - Show only running pods
- `/Error` - Show only error states

### 3. Multi-Namespace View
Press `0` to see resources across all namespaces

### 4. Resource Metrics
Press `Shift+F` to toggle resource usage display

### 5. Context Switching
Press `:ctx` to switch between Kubernetes contexts

## Troubleshooting

### Issue: k9s not connecting
**Solution**: Check kubectl context: `kubectl config current-context`

### Issue: Permission denied
**Solution**: Ensure your kubeconfig has proper permissions

### Issue: Resources not showing
**Solution**: Check namespace with `:ns` and switch if needed

### Issue: Slow performance
**Solution**: Increase refresh rate in config.yml

## Resources

- **Official Docs**: https://k9scli.io/
- **GitHub**: https://github.com/derailed/k9s
- **Cheat Sheet**: https://k9scli.io/topics/commands/

## Comparison: k9s vs kubectl

| Task | kubectl | k9s |
|------|---------|-----|
| List pods | `kubectl get pods` | `:pods` |
| Describe pod | `kubectl describe pod <name>` | Select + `d` |
| View logs | `kubectl logs <pod>` | Select + `l` |
| Delete pod | `kubectl delete pod <name>` | Select + `Ctrl+D` |
| Edit resource | `kubectl edit <resource>` | Select + `e` |
| Shell into pod | `kubectl exec -it <pod> -- sh` | Select + `s` |

**k9s is faster and more intuitive for interactive cluster management!**

---

**Cost**: $0/month (completely free)
**Setup Time**: < 5 minutes
**Learning Curve**: Easy (keyboard shortcuts)
**Recommendation**: ⭐⭐⭐⭐⭐ (5/5)
