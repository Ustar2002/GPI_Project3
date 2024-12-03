# GPI_Project3
Develop Your Own Physics Engine

## About Project

### Human Physics in pygame
- 경희대학교 컴퓨터공학과 게임프로그래밍입문 강의의 3번째 프로젝트
- 개발 기간: 2024.12.02 ~ 2024.12.14

게임 물리 엔진을 구현하기 위해 수업 시간에 배운 여러 내용을 적용해보았다. 구현 전에 unittest와 unittest.mock을 사용하는 테스트 주도 개발(TDD) 방법을 사용했다. 구현하고자 한 기술과 실제로 구현한 기능은 다음과 같다.
- 사람과 같이 복잡한 3D 오브젝트에 작은 물체(총알) 충돌 구현
- 총알, 화살, 불(화염 방사기), 가스, 수류탄 등 시뮬레이션 구현
- 사람 움직임 구현
- 충돌 시 반응 구현 (발 맞으면 발 사용 불가 등)
- 총 발사, 폭발 등에 대한 반동 구현
- 수류탄의 경우 던지면 땅에 몇번 튕기면서 굴러감. 일정 시간이 지나면 수류탄이 터지면서 파편이 나감.
- 위와 같은 방식으로 클레이모어도 구현
- 화살은 중력의 영향을 받아 포물선으로 나감
- 화염 방사기는 바람, 사용자의 이동에 영향을 받아 흔들림.
- 불이 붙을 수 있는 사물이 있다면 번지고, 발화하며 사물이 사라짐. 붙을 수 없는 상황이라면 더이상 번지지 않음.
- 연막탄의 경우 던지면 땅에 몇번 튕기면서 굴러감. 일정 시간이 지나면 연막탄에서 연막(가스)가 나오면서 주위에 퍼짐. 이 연막은 바람, 투사체 등등에 영향을 받아 흩어지거나 구멍이 생김.
- 물과 같은 유체, 바람과 같은 기체, 바위와 같은 고체 등을 이용하여 사람과 물체의 충돌 반응을 구현함.

- 스틱맨과 같이 간단한 리깅이 가능한 모델을 사용하여 위의 여러 기능들을 테스트(시뮬레이션).
- 스틱맨은 머리, 목, 몸, 팔, 손, 발 등 관절을 중심으로 히트 범위나 움직임을 나눔.

# Announcement

## 과제 설명
Pygame framework를 기초로 나만의 게임 엔진을 제작해봅시다.

중요한 평가 요소는 수업 및 실습에서 다룬 기능 및 기술을 도입하고 심화하여 하나의 프레임워크로 개발하는 것입니다.

완벽한 물리엔진을 만드는 것이 아니라 물리 엔진의 다양한 세부 요소 중에서 관심있고 구현해보고 싶은 기능들에 대한 개발 및 프로그래밍 경험을 해보는 것을 목표로 합니다.

물리 엔진의 기능을 가능한 많이 직접 구현해보고 본인이 구현한 기능을 표현할 수 있는 간단한 데모 프로그램을 작성하여 나만의 물리 엔진의 기능과 코드를 본인의 기여사항 위주로 설명해봅시다.

기 개발된 외부 물리엔진 라이브러리의 활용은 불가합니다. 즉, 이미 구현된 기능의 API를 활용하거나 library를 import하여 실행만 하는 것은 지양합니다. 이미 구현된 API나 open source를 활용해서 추가적인 기능을 구현하는 것을 지향합니다. 일반적인 계산 용도의 python관련 library 혹은 package는 활용 가능합니다.

## 일정 관련
- Project Consulting: 2024.11.28 17:00 – 18:15
(make up class & only those who want to participate)
- Presentation: 2024.12.10 - 2024.12.12 (3 min/student)
- Due Date: 2024.12.14 23:59:59 -> Upload to e-campus

## 주요 사항
- Submission: Code, Report, Short Execution Video, GitHub Link, Executable File 
- Report Contents: Physics Engine Design & Structure, Engine Features with Code Descriptions, Technical Implementation &
Contribution.
- Report Format: PDF -> All the other files in a “single” zip file.

## 평가지표
- 수업 및 실습에서 다룬 (혹은 더 심화된) 물리 엔진 관련 기술 중에서 본인이 선택한 요소에 대한 구현 및 기여사항
- 엔진 기술 개발 난이도 (30%)
- 엔진 기술 개발 필요성 (20%)
- 엔진 기술 개발 완성도 (50%)

## 구현 기능 예시 (하단 리스트로 제한하지는 않고 더 제안 가능)
A. Reference Text Book: Game Engine Architecture & Real-time Collision Detection

B. Collision Detection: GJK collision detection, SAT, OBB, Moving Objects, Concave Object, Bounding volume hierarchy, Convex Hull Algorithm, Optimization, …

C. Rigid Body Dynamics

D. Impulsive Collision Response (with Torque)

E. Particle System & Simulation: fluid, smoke, fire, explosion,…

F. Numerical Methods: modified Euler method, RK4, Verlet Integration, Velocity Verlet, …

G. Model Deformation (Free-form Deformation)

H. Deformable Body