# bot - set up

## 1. catkin_ws 빌드
`bot` 폴더를 `~/catkin_ws/src/`에 복사

```bash
cd ~/catkin_ws
catkin_make_isolated --install
```

## 2. bashrc 설정
`setup/bashrc`의 내용을 `~/.bashrc`에 복사

```bash
cat ~/catkin_ws/src/bot/setup/bashrc >> ~/.bashrc
source ~/.bashrc
```

## 3. udev 설정
```bash
sudo cp ~/catkin_ws/src/bot/setup/99-usb-serial.rules /etc/udev/rules.d/
```

## 4. 부팅 시 자동 실행 service 등록
- `$HOME` 경로에 `setup/bot.sh` 추가: `/home/sokim/bot.sh`
- `/etc/systemd/system/` 경로에 `bot.service` 추가: `/etc/systemd/system/bot.service`

```bash
cp ~/catkin_ws/src/bot/setup/bot.sh ~/bot.sh
chmod +x ~/bot.sh

sudo cp ~/catkin_ws/src/bot/setup/bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl start bot.service
```

- 상태 확인:

```bash
sudo systemctl status bot
sudo service bot restart
journalctl -fu bot -o cat  # 로그 확인
```

- systemd 없이 직접 실행하려면:
```bash
roslaunch bot_bringup start.launch
```

## 5. Nav/SLAM 모드 전환
- `start.launch`(또는 `bot.service`)가 실행 중인 상태에서 `bashrc`의 alias로 모드를 변경할 수 있음
- 기본값은 NAV 모드

| 명령어 | 설명 |
|---|---|
| `nav`   | 네비게이션 모드 |
| `slam`  | SLAM 모드 (Cartographer) |
| `reset` | 시스템 재시작 |

- SLAM만 단독으로 띄우려면 별도 launch로 실행 가능:
```bash
roslaunch bot_slam cartographer.launch.xml
```

## 6. SLAM 중 맵 저장
- 저장 결과는 `$ROS_DB_PATH/map/`에 생성됨.
```bash
rosservice call /save_map "save_in_db: false"
```
