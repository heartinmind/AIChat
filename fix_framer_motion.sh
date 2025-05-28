#!/bin/bash

# framer-motion TypeScript 문제 해결 스크립트

echo "🔧 framer-motion TypeScript 문제 해결"
echo "====================================="
echo ""

cd /Users/unipurple/Projects/AIChat/admin

# 1. TypeScript 캐시 정리
echo "1. TypeScript 캐시 정리..."
rm -rf node_modules/.cache
rm -rf tsconfig.tsbuildinfo
rm -rf .eslintcache

# 2. framer-motion 재설치
echo ""
echo "2. framer-motion 재설치..."
npm uninstall framer-motion
npm install framer-motion@latest --save

# 3. TypeScript 버전 확인 및 업데이트
echo ""
echo "3. TypeScript 버전 확인..."
npm list typescript
npm install typescript@4.9.5 --save-dev

# 4. @types/react 확인
echo ""
echo "4. React 타입 정의 확인..."
npm install @types/react@latest @types/react-dom@latest --save-dev

# 5. moduleResolution 확인
echo ""
echo "5. tsconfig.json 백업 및 수정..."
cp tsconfig.json tsconfig.json.backup

# moduleResolution을 bundler로 변경 시도
cat > tsconfig.temp.json << 'EOL'
{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": ".",
    "paths": {
      "*": ["node_modules/*"]
    }
  },
  "include": [
    "src"
  ]
}
EOL

mv tsconfig.temp.json tsconfig.json

# 6. Frontend 재시작
echo ""
echo "6. Frontend 재시작..."
pkill -f "react-scripts start" 2>/dev/null
sleep 2

PORT=3001 npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..
echo $FRONTEND_PID > .frontend.pid

echo ""
echo "====================================="
echo "✅ 수정 완료!"
echo ""
echo "Frontend가 재시작되었습니다."
echo "브라우저에서 http://localhost:3001 확인하세요."
echo ""
echo "문제가 지속되면:"
echo "1. VSCode/에디터를 재시작하세요"
echo "2. tail -f frontend.log 로 로그를 확인하세요"
