편수	제목 또는 주제	상태	주요 내용 요약
1편	Why I'm Building Pentra	✅ 완료	보안 제품이 아닌 행위 서사의 필요성, Pentra 철학 소개
2편	On Language and Security: Why Pentra Needed a New Way to Describe Threats	✅ 완료	DSL 설계 철학, Sigma와의 차이점, 해석 기반 언어의 의의
3편	Sessions, Roles, and the Shape of Threats	🔜 예정	세션 빌더, 역할 평가기, TTP 체이닝 흐름 분석 구조
4편	Reconstructing Attack Paths: From Logs to Narrative Chains	🟡 설계됨	전체 로그 흐름을 E2E 공격 서사로 복원하는 과정 설명
5편	Designing for Intent: Why Pentra Treats Policy as Evidence	🟡 설계됨	정책 감사기를 증거 해석기로 보는 철학, snapshot 기반 감사 설명
6편	Between Simulation and Explanation: Where Pentra Might Go Next	🟡 설계됨	향후 기능 (AI hook, 공격 시뮬레이터, 리포터) 미래 청사진 공유

📌 각 편 역할 요약
그룹	구성	역할
철학/배경	1~2편	Pentra의 출발 이유, 언어 철학
기술 구현	3~5편	세션 구조, 경로 재구성, 정책 감사
비전/전망	6편	향후 AI, Sim, SaaS화, 제품화 방향

🧩 3편 이후 흐름 제안
편수	발행 시기 제안	        이유
3편	🔜 5월 말 이전       	2편과 흐름 연결 + 실제 구현된 평가기 기반
4편	6월 중순               	E2E 경로 재구성 및 리포팅 프로토타입 나올 때
5편	6월 말~7월 초           	정책 감사기 구조 완성 이후
6편	하반기 발표 전	        컨퍼런스/논문/제품화 구상 타이밍에 맞춰


축	설명	Pentra에서의 구현 요소
1. 로그 → 세션으로	단순히 시간순이 아닌 맥락 기반 그룹화	build_sessions() – src_ip + dst_ip + username 기준
2. 세션의 의미	Pentra는 세션을 단순 그룹이 아닌 행위 단위로 해석	세션을 하나의 “의미 단위”로 보고 평가 흐름 적용
3. 역할 평가기 (evaluate_role)	세션 내 이벤트마다 entrypoint, pivotable, expansion 등의 역할을 부여	session_roles.yaml 기반 DSL + 조건 평가기
4. 체이닝 평가기 (evaluate_ttp_chain)	세션 내 TTP 흐름을 시퀀스화하고, 고유 TTP 개수 + confidence 도출	TTP 추출 → 중복 제거 → 흐름 분석
5. 흐름이 갖는 의미	Pentra는 로그를 보는 것이 아니라 형태(Shape) 를 봄	단순 탐지가 아닌 “서사” 복원 의도
6. DSL 기반 해석 구조의 결합	앞서 설명한 DSL이 실제 어떻게 평가기에 쓰이는지 초기 연결 설명	간단한 예시 1~2개 포함 가능 (기밀 유지 조건 하에)