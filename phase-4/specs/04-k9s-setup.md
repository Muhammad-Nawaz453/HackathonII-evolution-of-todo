# Specification: k9s Setup and Usage

**Feature ID**: PHASE4-04
**Status**: Draft
**Created**: 2026-02-08
**Dependencies**: Phase 4 Spec 02 (Kubernetes Design)

## Purpose

Integrate k9s, a free and open-source terminal UI for Kubernetes, to provide an intuitive, interactive interface for cluster management. k9s eliminates the need for paid AI-powered tools while offering a superior user experience for monitoring, debugging, and managing Kubernetes resources.

**🎉 100% FREE - No API keys, no paid services, no credit card required!**

## User Stories

**As a DevOps engineer**, I want to:
1. Visually monitor cluster state in real-time
2. Quickly navigate between different resource types
3. Debug issues using keyboard shortcuts
4. View logs and describe resources without typing long commands
5. Edit and delete resources interactively
6. Use a tool that works offline and has no rate limits

**As a developer**, I want to:
1. Check pod status with a visual interface
2. Stream logs in real-time with easy navigation
3. Shell into pods for debugging
4. Understand resource relationships visually
5. Learn Kubernetes concepts through an intuitive UI

## Acceptance Criteria

### AC1: k9s Installation
- [ ] k9s installed on development machine
- [ ] k9s accessible via `k9s` command
- [ ] Version verification works (`k9s version`)
- [ ] No API keys or paid services required
- [ ] Works offline after installation

### AC2: Configuration
- [ ] Configuration file created (~/.k9s/config.yml)
- [ ] Default namespace set to todo-app-dev
- [ ] Refresh rate configured (2 seconds)
- [ ] Mouse support enabled
- [ ] Favorite namespaces configured
- [ ] Custom aliases set up (optional)

### AC3: Basic Operations
- [ ] View all pods: `:pods` or `:po`
- [ ] View services: `:services` or `:svc`
- [ ] View deployments: `:deployments` or `:deploy`
- [ ] View logs: Select resource + `l`
- [ ] Describe resource: Select resource + `d`
- [ ] View YAML: Select resource + `y`

### AC4: Advanced Operations
- [ ] Shell into pod: Select pod + `s`
- [ ] Edit resource: Select resource + `e`
- [ ] Delete resource: Select resource + `Ctrl+D`
- [ ] Scale deployment: Select deployment + `s`
- [ ] Filter resources: Press `/` and type filter
- [ ] View all namespaces: Press `0`

### AC5: Debugging Workflows
- [ ] Identify failing pods (red status indicators)
- [ ] View pod events and logs
- [ ] Check resource usage (CPU, memory)
- [ ] Trace service endpoints
- [ ] Monitor deployment rollouts
- [ ] View ConfigMaps and Secrets

### AC6: Performance and Usability
- [ ] Real-time updates (< 2 second refresh)
- [ ] Keyboard navigation is fast and responsive
- [ ] No lag or performance issues
- [ ] Works with Minikube cluster
- [ ] Context switching works (`:ctx`)
- [ ] Help system accessible (`?`)

## Technical Design

### Installation Methods

#### Windows
```bash
# Via Chocolatey
choco install k9s

# Via Scoop
scoop install k9s

# Via Binary Download
# Download from: https://github.com/derailed/k9s/releases
# Extract and add to PATH
```

#### macOS
```bash
# Via Homebrew
brew install k9s

# Via Binary Download
curl -sS https://webinstall.dev/k9s | bash
```

#### Linux
```bash
# Via Package Manager
sudo apt install k9s        # Ubuntu/Debian
sudo pacman -S k9s          # Arch Linux
sudo dnf install k9s        # Fedora

# Via Binary Download
curl -sS https://webinstall.dev/k9s | bash
```

### Configuration File

**File**: `~/.k9s/config.yml`

```yaml
k9s:
  # Refresh rate in seconds
  refreshRate: 2

  # Max connection retries
  maxConnRetry: 5

  # Enable mouse support
  enableMouse: true

  # Read-only mode (safety)
  readOnly: false

  # Default namespace
  namespace:
    active: todo-app-dev
    favorites:
      - todo-app-dev
      - todo-app-prod
      - default
      - kube-system

  # UI settings
  ui:
    enableMouse: true
    headless: false
    logoless: false
    crumbsless: false
    noIcons: false
    reactive: true
    skin: default

  # Log settings
  logger:
    tail: 200
    buffer: 5000
    sinceSeconds: 300
    fullScreen: false
    textWrap: false
    showTime: true

  # Thresholds for resource usage colors
  thresholds:
    cpu:
      critical: 90
      warn: 70
    memory:
      critical: 90
      warn: 70
```

### Essential Keyboard Shortcuts

#### Navigation
- `:` - Command mode (type resource name)
- `/` - Filter/search current view
- `Esc` - Back/cancel
- `?` - Help (shows all shortcuts)
- `Ctrl+A` - Show all available resources
- `Ctrl+R` - Refresh view

#### Resource Management
- `d` - Describe selected resource
- `l` - View logs
- `e` - Edit resource (opens in editor)
- `y` - View YAML
- `Ctrl+D` - Delete resource (with confirmation)
- `s` - Shell into pod or scale deployment

#### View Controls
- `0` - Show all namespaces
- `1-9` - Show specific namespace
- `Ctrl+S` - Save current view
- `Ctrl+Z` - Toggle wide columns
- `Shift+F` - Toggle resource usage display

#### Logs
- `l` - View logs
- `p` - Previous logs (for crashed containers)
- `f` - Toggle follow mode
- `w` - Toggle wrap
- `t` - Toggle timestamps
- `c` - Clear logs

### Common Workflows

#### 1. Monitor Cluster Health
```
1. Launch: k9s
2. View pods: :pods
3. Check status (green = healthy, red = failing)
4. Press Shift+F to see resource usage
5. Press 0 to see all namespaces
```

#### 2. Debug Failing Pod
```
1. Launch: k9s -n todo-app-dev
2. Navigate to failing pod (red status)
3. Press 'd' to describe (see events)
4. Press 'l' to view logs
5. Press 'p' for previous logs (if crashed)
6. Press 's' to shell into pod (if running)
```

#### 3. Scale Deployment
```
1. Type: :deploy
2. Navigate to deployment
3. Press 's' to scale
4. Enter desired replica count
5. Press Enter to confirm
```

#### 4. View Service Endpoints
```
1. Type: :svc
2. Navigate to service
3. Press 'd' to describe
4. View endpoints, ports, and selectors
```

#### 5. Check Resource Usage
```
1. Type: :pods
2. Press Shift+F to show CPU/memory
3. Sort by usage (arrow keys)
4. Identify resource-hungry pods
```

#### 6. View Logs Across Pods
```
1. Type: :pods
2. Filter by label: /app=backend
3. Select pod
4. Press 'l' for logs
5. Press 'f' to follow
6. Press 't' to show timestamps
```

### Integration with Phase 4

#### Minikube Context
```bash
# Ensure k9s connects to Minikube
kubectl config use-context minikube
k9s

# Or specify context directly
k9s --context minikube
```

#### Namespace Setup
```bash
# Launch k9s in todo-app-dev namespace
k9s -n todo-app-dev

# Or switch namespace inside k9s
# Press ':ns' and select namespace
```

#### Monitoring Deployment
```bash
# After deploying with Helm
k9s -n todo-app-dev

# Check:
# 1. All pods are Running (green)
# 2. Services have endpoints
# 3. Deployments have desired replicas
# 4. No error events
```

## Advantages Over Paid Alternatives

### k9s (FREE) vs kubectl-ai (PAID)

| Feature | k9s | kubectl-ai |
|---------|-----|------------|
| Cost | $0/month | ~$20-50/month (OpenAI API) |
| API Key | Not required | Required |
| Internet | Not required | Required |
| Speed | Instant | 1-3 seconds per query |
| Rate Limits | None | Yes (OpenAI limits) |
| Offline | Works offline | Requires internet |
| Learning Curve | Easy (keyboard shortcuts) | Natural language |
| Reliability | 100% uptime | Depends on API |

### k9s (FREE) vs kagent (PAID)

| Feature | k9s | kagent |
|---------|-----|--------|
| Cost | $0/month | ~$50-100/month (OpenAI API) |
| Setup | 5 minutes | 30+ minutes |
| Monitoring | Real-time visual | Background agent |
| Auto-healing | Manual | Automatic |
| Control | Full control | AI decides |
| Transparency | See everything | Black box |
| Safety | Confirmation prompts | Auto-actions (risky) |

## Testing Checklist

- [ ] k9s installs successfully
- [ ] k9s connects to Minikube cluster
- [ ] Can view all resource types
- [ ] Keyboard shortcuts work
- [ ] Log streaming works
- [ ] Pod shell access works
- [ ] Resource editing works
- [ ] Filtering and search work
- [ ] Context switching works
- [ ] Configuration file loads
- [ ] Performance is acceptable
- [ ] No errors or crashes

## Documentation

### Quick Reference Card

Create a quick reference card for common tasks:

```
┌─────────────────────────────────────────────────────────┐
│              k9s Quick Reference                         │
├─────────────────────────────────────────────────────────┤
│ Launch:        k9s                                       │
│ Help:          ?                                         │
│ Quit:          Ctrl+C or :quit                          │
├─────────────────────────────────────────────────────────┤
│ Resources:                                               │
│   :pods        :svc         :deploy      :ing           │
│   :cm          :sec         :ns          :ctx           │
├─────────────────────────────────────────────────────────┤
│ Actions:                                                 │
│   d - Describe    l - Logs       s - Shell/Scale        │
│   e - Edit        y - YAML       Ctrl+D - Delete        │
├─────────────────────────────────────────────────────────┤
│ Navigation:                                              │
│   / - Filter      0 - All NS     Esc - Back            │
│   Shift+F - Usage Ctrl+R - Refresh                      │
└─────────────────────────────────────────────────────────┘
```

### Training Materials

Include in documentation:
1. Installation guide (all platforms)
2. Configuration examples
3. Keyboard shortcut cheat sheet
4. Common workflow tutorials
5. Troubleshooting guide
6. Video demo (optional)

## Success Criteria

k9s integration is complete when:
- ✅ k9s installed and configured
- ✅ Can monitor all Phase 4 resources
- ✅ All common workflows documented
- ✅ Team trained on basic usage
- ✅ Quick reference card created
- ✅ No paid tools required
- ✅ Works offline
- ✅ Performance is excellent

## Maintenance

### Updates
```bash
# Update k9s to latest version
# Windows (Chocolatey)
choco upgrade k9s

# macOS (Homebrew)
brew upgrade k9s

# Linux
# Download latest binary from GitHub
```

### Configuration Backup
```bash
# Backup k9s config
cp ~/.k9s/config.yml ~/.k9s/config.yml.backup

# Restore config
cp ~/.k9s/config.yml.backup ~/.k9s/config.yml
```

## Resources

- **Official Website**: https://k9scli.io/
- **GitHub Repository**: https://github.com/derailed/k9s
- **Documentation**: https://k9scli.io/topics/
- **Cheat Sheet**: https://k9scli.io/topics/commands/
- **Community**: GitHub Discussions

---

**Cost**: $0/month (completely free)
**Setup Time**: < 5 minutes
**Learning Curve**: Easy (1-2 hours to master)
**Recommendation**: ⭐⭐⭐⭐⭐ (5/5)
**Status**: Ready for Implementation
