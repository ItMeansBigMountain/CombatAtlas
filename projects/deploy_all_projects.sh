#!/bin/bash
# Deploy all projects via Vercel

PROJECTS_DIR="/data/OpEnCLAw"
PROJECTS=$(ls -1 "$PROJECTS_DIR" | grep -v "^\." | grep -v "PROJECT" | grep -v "SECURITY" | grep -v "legacy-" | grep -v "additional" | grep -v "coding-school" | grep -v "consumer" | grep -v "honda" | grep -v "journal" | grep -v "api.requests" | grep -v "bitcoin" | grep -v "addictive" | grep -v "docs" | grep -v "README" | grep -v "legacy-modernization" | grep -v "legacy-code" | grep -v "additional-source" | grep -v "vercel-urls" | grep -v "WORKLOG" | grep -v "MEMORY" | grep -v "HEARTBEAT" | grep -v "SOUL" | grep -v "IDENTITY" | grep -v "USER" | grep -v "AGENTS" | grep -v "work-queue" | grep -v "finished-work" | grep -v "TOOLS" | grep -v "STATUS" | grep -v "package-lock" | grep -v "null" | grep -v "function")

for project in $PROJECTS; do
  echo "=== Processing $project ==="
  PROJECT_PATH="$PROJECTS_DIR/$project"
  
  # Check for package.json
  if [ -f "$PROJECT_PATH/package.json" ]; then
    echo "Found package.json - checking for Vercel compatibility"
    if grep -q "vercel" "$PROJECT_PATH/package.json" || grep -q "vercel" "$PROJECT_PATH/vercel.json"; then
      echo "Deploying $project via Vercel"
      # vercel deploy
    else
      echo "$project needs Vercel configuration"
    fi
  fi
  
  # Check for project-specific deployment files
  if [ -f "$PROJECT_PATH/.vercel" ] || [ -f "$PROJECT_PATH/vercel.json" ]; then
    echo "$project is Vercel-configured"
  fi
  
done
echo "Done"
