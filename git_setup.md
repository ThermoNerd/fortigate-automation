# Git Setup Instructions

1. First, restart your PowerShell/Terminal

2. Configure Git with your information (replace with your details):
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

3. Initialize the repository and push to GitHub:
```powershell
# Initialize repository
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: FortiGate status monitoring script"

# Create main branch
git branch -M main
```

4. Go to GitHub.com:
   - Sign in or create an account
   - Click the '+' in the top right
   - Select 'New repository'
   - Name it 'fortigate-automation'
   - Leave it public
   - Don't initialize with README (we already have one)
   - Click 'Create repository'

5. After creating the repository, run these commands (replace YOUR_USERNAME):
```powershell
git remote add origin https://github.com/YOUR_USERNAME/fortigate-automation.git
git push -u origin main
```

Note: When you run the push command, you'll need to authenticate with GitHub. Follow the browser prompts to complete the authentication.
