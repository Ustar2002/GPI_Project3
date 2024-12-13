# GPI_Project3
Develop Your Own Physics Engine

## About Project

### Pygame 기반 실시간 물리 시뮬레이션 엔진 개발

- **강의**: 경희대학교 컴퓨터공학과 게임프로그래밍입문 강의 3번째 프로젝트
- **개발 기간**: 2024.12.02 ~ 2024.12.14

본 프로젝트는 Pygame 프레임워크를 활용하여 커스텀 물리 엔진을 설계하고 구현하는 것을 목표로 하였다. 수업 시간에 배운 물리 개념과 프로그래밍 기법을 직접 적용하여 다양한 발사체와 물리적 상호작용을 포함하는 인터랙티브한 시뮬레이션을 구현하였다. 특히, 다음과 같은 주요 기능들을 직접 구현하고 심화하였다:

- **다양한 발사체 시뮬레이션**:
  - **총(Projectile)**: 중력과 바람의 영향을 받지 않는 직선 운동을 하는 발사체로, 마우스 클릭 방향으로 발사된다.
  - **화살(Arrow)**: 중력과 바람의 영향을 받아 포물선 궤적을 그리며, 충돌 시 그 지점에 꽂혀 정지한다.
  - **수류탄(Grenade)**: 중력과 바람의 영향을 받아 자유 낙하 및 튕김을 반복하며, 일정 시간이 지나면 폭발하여 다수의 파편(Fragment)을 생성한다.

- **강체 역학(Rigid Body Dynamics)**:
  - **버스(RigidBodyObject)**: 질량과 관성 모멘트를 고려한 직사각형 강체로, 발사체 및 파편과의 충돌 시 임펄스와 토크를 적용하여 회전과 이동을 반영한다.
  - **관성 모멘트(Inertia)**: 버스의 회전에 대한 저항을 나타내는 관성 모멘트를 계산하여, 충돌 시 각속도의 변화를 구현하였다.

- **파티클 시스템(Particle System)**:
  - **비(Particle)**: 우클릭으로 토글 가능한 비가 화면 상단에서 생성되어 바닥에 도달하면 물 웅덩이를 형성하고, 물 웅덩이 수준에 따라 마찰력이 변화한다.
  - **파편(Fragment)**: 수류탄 폭발 시 생성되어 랜덤한 방향과 속도로 퍼져나가며, 버스와의 충돌 시 소멸되고 버스에 임펄스를 부여한다.

- **환경 요소(Environmental Forces)**:
  - **바람(Wind)**: E 키로 바람을 토글하고, 1~8 키로 바람의 방향을 설정하며, 9/0 키로 바람의 세기를 조절하여 바람이 발사체와 파티클의 운동에 실시간으로 영향을 미친다.

- **UI 및 상호작용**:
  - **무기 스위칭**: Q 키로 총, 수류탄, 화살 모드를 순환 전환할 수 있으며, 현재 선택된 무기는 반투명 UI 패널에 두 줄로 직관적으로 표시된다.
  - **발사 메커니즘**: 마우스 좌클릭으로 현재 선택된 무기를 발사하며, 좌클릭 시 무기 종류에 따라 발사체의 동작이 다르게 구현된다.
  - **정보 표시**: 반투명 UI 패널에 현재 무기, 바람 상태(방향 및 세기), 물 웅덩이 수준 등을 두 줄로 명확하게 표시하여 사용자에게 직관적인 정보를 제공한다.

- **기타 기능**:
  - **플레이어 이동**: 화살표 키 또는 WASD 키를 사용하여 플레이어 스폰 포인트를 이동시킬 수 있다.
  - **리셋 기능**: R 키로 게임을 초기 상태로 리셋하여 모든 오브젝트와 환경 상태를 초기화할 수 있다.
  - **비 토글**: 우클릭으로 비를 활성화하거나 비활성화할 수 있으며, 비가 활성화되면 상단에서 비 파티클이 지속적으로 생성된다.

본 프로젝트는 수업에서 배운 물리적 개념들을 실제 코드로 구현함으로써 물리 엔진의 기본적인 구조와 기능들을 이해하고, 이를 바탕으로 다양한 시뮬레이션을 구현하는 경험을 제공하였다. 특히, 강체 역학, 임펄스 충돌 응답, 파티클 시스템과 같은 핵심 물리 개념들을 직접 구현하여 물리 엔진 개발에 대한 실질적인 이해를 높였다.

## Announcement

### 과제 설명
Pygame framework를 기초로 나만의 게임 엔진을 제작해봅시다.

중요한 평가 요소는 수업 및 실습에서 다룬 기능 및 기술을 도입하고 심화하여 하나의 프레임워크로 개발하는 것입니다.

완벽한 물리엔진을 만드는 것이 아니라 물리 엔진의 다양한 세부 요소 중에서 관심있고 구현해보고 싶은 기능들에 대한 개발 및 프로그래밍 경험을 해보는 것을 목표로 합니다.

물리 엔진의 기능을 가능한 많이 직접 구현해보고 본인이 구현한 기능을 표현할 수 있는 간단한 데모 프로그램을 작성하여 나만의 물리 엔진의 기능과 코드를 본인의 기여사항 위주로 설명해봅시다.

기 개발된 외부 물리엔진 라이브러리의 활용은 불가합니다. 즉, 이미 구현된 기능의 API를 활용하거나 library를 import하여 실행만 하는 것은 지양합니다. 이미 구현된 API나 open source를 활용해서 추가적인 기능을 구현하는 것을 지향합니다. 일반적인 계산 용도의 python관련 library 혹은 package는 활용 가능합니다.

### 일정 관련
- **Project Consulting**: 2024.11.28 17:00 – 18:15  
  (make up class & only those who want to participate)
- **Presentation**: 2024.12.10 - 2024.12.12  
  (3 min/student)
- **Due Date**: 2024.12.14 23:59:59  
  -> Upload to e-campus

### 주요 사항
- **Submission**: Code, Report, Short Execution Video, GitHub Link, Executable File 
- **Report Contents**: Physics Engine Design & Structure, Engine Features with Code Descriptions, Technical Implementation & Contribution.
- **Report Format**: PDF -> All the other files in a “single” zip file.

### 평가지표
- 수업 및 실습에서 다룬 (혹은 더 심화된) 물리 엔진 관련 기술 중에서 본인이 선택한 요소에 대한 구현 및 기여사항
- 엔진 기술 개발 난이도 (30%)
- 엔진 기술 개발 필요성 (20%)
- 엔진 기술 개발 완성도 (50%)

### 구현 기능 예시 (하단 리스트로 제한하지는 않고 더 제안 가능)
A. Reference Text Book: Game Engine Architecture & Real-time Collision Detection

B. Collision Detection: GJK collision detection, SAT, OBB, Moving Objects, Concave Object, Bounding volume hierarchy, Convex Hull Algorithm, Optimization, …

C. Rigid Body Dynamics

D. Impulsive Collision Response (with Torque)

E. Particle System & Simulation: fluid, smoke, fire, explosion,…

F. Numerical Methods: modified Euler method, RK4, Verlet Integration, Velocity Verlet, …

G. Model Deformation (Free-form Deformation)

H. Deformable Body
