#!/bin/bash

echo "🚀 Creating Azure DevOps Pipeline..."

# Create the pipeline
az pipelines create \
  --name "Sustainability Analysis Pipeline" \
  --description "Code sustainability analysis with visual reporting" \
  --repository Alpha \
  --branch main \
  --yaml-path azure-pipelines.yml \
  --organization https://dev.azure.com/159645 \
  --project Alpha

echo "✅ Pipeline created successfully!"
echo "📊 Check your pipeline at: https://dev.azure.com/159645/Alpha/_build"