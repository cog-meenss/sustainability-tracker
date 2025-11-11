# 📦 Project Type Configuration Templates

This directory contains pre-configured templates for different project types to make the sustainability pipeline instantly usable across various technology stacks.

## 🎯 Available Templates

### 1. Python Projects
**File**: `python-project-config.yml`
**Best for**: Django, Flask, FastAPI, data science, CLI tools
**Features**: 
- Python-specific analysis tools (Bandit, Safety, Radon)
- Virtual environment detection  
- Package security scanning
- Memory usage optimization

### 2. JavaScript/Node.js Projects  
**File**: `javascript-project-config.yml`
**Best for**: React, Vue, Angular, Node.js servers, npm packages
**Features**:
- ESLint integration
- npm audit security scanning  
- Bundle size analysis
- Performance monitoring

### 3. Full-Stack Projects
**File**: `fullstack-project-config.yml`  
**Best for**: Projects with both frontend and backend
**Features**:
- Multi-language analysis
- Comprehensive dependency scanning
- API performance testing
- Database query optimization

### 4. Java Projects
**File**: `java-project-config.yml`
**Best for**: Spring Boot, Maven/Gradle projects
**Features**:
- SpotBugs integration
- JVM performance analysis
- Dependency vulnerability scanning
- Memory leak detection

### 5. Go Projects  
**File**: `go-project-config.yml`
**Best for**: Microservices, CLI tools, web services
**Features**:
- go vet integration
- Performance profiling
- Binary size optimization
- Concurrency analysis

### 6. Microservice Architecture
**File**: `microservice-config.yml`
**Best for**: Containerized services, Kubernetes deployments  
**Features**:
- Container optimization
- Service mesh analysis
- Resource usage monitoring
- API efficiency checking

### 7. Library/Package Projects
**File**: `library-project-config.yml`
**Best for**: Shared libraries, npm/PyPI packages
**Features**:
- Higher quality thresholds
- Documentation requirements
- API compatibility checking
- Distribution optimization

### 8. Enterprise Projects
**File**: `enterprise-config.yml`
**Best for**: Large organizations with compliance requirements
**Features**:
- Strict security requirements
- Compliance reporting
- Audit trail generation
- Multi-team coordination

## 🚀 Usage

### Quick Setup
```bash
# Copy appropriate template to your project
cp reusability-templates/python-project-config.yml .sustainability/config.yml

# Or use the deployment script with project type
./deploy-sustainability.sh python my-python-project
```

### Template Structure
Each template includes:
- **Analysis configuration** tailored to the technology stack
- **Quality thresholds** appropriate for the project type  
- **Tool selections** optimized for the language/framework
- **Reporting preferences** suited to the development workflow
- **Notification settings** aligned with team practices

## 🔧 Customization

All templates can be customized by:
1. Copying to `.sustainability/config.yml`
2. Modifying thresholds and settings
3. Adding project-specific exclusions
4. Configuring team notification preferences

## 📊 Template Comparison

| Project Type | Sustainability | Security | Performance | Documentation |
|--------------|----------------|----------|-------------|---------------|
| Python       | 60/100        | 75/100   | 65/100      | 70/100        |
| JavaScript   | 65/100        | 70/100   | 70/100      | 65/100        |
| Full-Stack   | 70/100        | 80/100   | 75/100      | 75/100        |
| Java         | 65/100        | 80/100   | 70/100      | 80/100        |
| Go           | 70/100        | 75/100   | 80/100      | 70/100        |
| Microservice | 75/100        | 85/100   | 85/100      | 80/100        |
| Library      | 80/100        | 85/100   | 80/100      | 90/100        |
| Enterprise   | 85/100        | 95/100   | 85/100      | 85/100        |

## 🌟 Benefits of Using Templates

### ✅ **Instant Setup**
- Pre-configured for specific technology stacks
- No guesswork on appropriate thresholds
- Industry-standard tool selections

### ✅ **Best Practices**  
- Curated by sustainability experts
- Regular updates with community feedback
- Proven configurations from real projects

### ✅ **Consistency**
- Standardized across similar project types
- Easy team adoption and onboarding
- Comparable metrics across projects

### ✅ **Flexibility**
- Easy to customize for specific needs  
- Extensible for additional requirements
- Backwards compatible with updates

Choose the template that best matches your project type to get started with optimal sustainability analysis configuration!