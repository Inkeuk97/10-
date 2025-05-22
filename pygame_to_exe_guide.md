# 🎮 Pygame 게임을 EXE 파일로 변환하기

이 문서는 Python의 Pygame으로 만든 게임을 `.exe` 실행 파일로 변환하는 과정을 안내합니다. `PyInstaller`를 사용하여 Windows에서 실행 가능한 파일을 생성합니다.

---

## ✅ 사전 준비

- Python이 설치되어 있어야 합니다.
- 게임 코드가 완성되어 있어야 합니다 (예: `main.py`).
- 필요한 외부 리소스(이미지, 사운드 등)는 코드에서 상대 경로로 불러오도록 구성합니다.

---

## 1. PyInstaller 설치

터미널 또는 명령 프롬프트에서 다음 명령어를 입력하여 PyInstaller를 설치합니다:

```bash
pip install pyinstaller
```

---

## 2. EXE 파일 생성

다음 명령어를 실행하여 `.exe` 파일을 생성합니다:

```bash
pyinstaller --onefile --windowed main.py
```

### 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--onefile` | 모든 파일을 하나의 실행 파일로 압축 |
| `--windowed` | 콘솔 창 없이 실행 (GUI 프로그램용) |

예를 들어 `brick_game.py`라는 파일을 변환하려면:

```bash
pyinstaller --onefile --windowed brick_game.py
```

---

## 3. 결과물 확인

변환이 완료되면 다음과 같은 폴더들이 생성됩니다:

```
📁 dist/
  └── main.exe         ← 최종 실행 파일
📁 build/
📄 main.spec            ← 빌드 설정 파일
```

- `dist/` 폴더 안의 `.exe` 파일이 최종 결과물입니다.
- 외부 이미지나 사운드 파일이 있다면 `.exe` 파일과 같은 폴더에 넣어야 합니다.

---

## 4. 아이콘 추가 (선택사항)

아이콘이 있는 `.ico` 파일을 준비한 후 다음처럼 실행하세요:

```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

---

## 5. GUI 기반 빌드 도구 사용 (선택사항)

GUI 환경에서 쉽게 `.exe`를 만들고 싶다면 `auto-py-to-exe`를 설치해보세요:

```bash
pip install auto-py-to-exe
auto-py-to-exe
```

이후 GUI 창에서 옵션을 설정하고 변환할 수 있습니다.

---

## ✅ 참고사항

- `.exe` 파일은 Windows에서만 실행됩니다.
- 처음 실행 시 다소 느릴 수 있습니다 (압축 해제 때문).
- 바이러스 오탐지로 인해 경고가 발생할 수 있습니다 (배포 시 주의).

---

## 📦 배포 팁

- 외부 리소스가 있다면 `.exe`와 같은 폴더에 포함시켜 전달하세요.
- 전체를 `.zip`으로 압축하여 공유하면 편리합니다.