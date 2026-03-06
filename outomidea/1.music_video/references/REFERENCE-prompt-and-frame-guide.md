# REFERENCE: Prompt & Frame Guide

> **버전**: v1.0  
> **용도**: SKILL-1(v4) 에이전트가 S3(콘티 프레임 지시서) 및 S4(7블록 프롬프트) 생성 시 참조  
> **사용법**: 각 Part의 키워드 테이블에서 장면의 감정/맥락에 맞는 키워드를 선택하여 prompt_seed 또는 7블록에 삽입  
> **최종 갱신**: 2026-03-01

---

## Part 1: SUBJECT — 표정 & 포즈 키워드

### 1.1 표정(Facial Expression) — 감정 계열별

> S3 `character_direction.expression`과 S4 `[SUBJECT]` 블록에 삽입

#### 슬픔 계열

| 영문 키워드 | 얼굴 변화 | 감정 맥락 | 추천 조명 | 추천 샷 |
|---|---|---|---|---|
| `teary-eyed expression` | 눈 충혈, 눈물 맺힘, 아래 입술 떨림 | 이별 직전, 참는 울음 | soft side-light, cool-blue rim | CU |
| `quietly weeping face` | 눈물 흐름, 눈썹 내려감, 코 붉어짐 | 혼자 우는 밤 | dim warm backlight | ECU |
| `heartbroken expression` | 미간 주름, 입꼬리 아래, 초점 잃은 눈 | 배신, 상실 | desaturated ambient | MCU |
| `melancholic gaze` | 눈꺼풀 반쯤 처짐, 먼 곳 응시 | 추억 회상, 그리움 | golden hour backlight, fog | MCU |
| `wistful look` | 눈가 당김, 고개 약간 아래, 반쯤 미소+슬픔 | 지나간 것에 대한 아쉬움 | soft dusk light, warm amber | CU |
| `dejected face` | 눈썹 완전 아래, 고개 숙임 | 실패, 포기, 무기력 | overcast flat light, cool-gray | MS |

#### 분노 계열

| 영문 키워드 | 얼굴 변화 | 감정 맥락 | 추천 조명 | 추천 샷 |
|---|---|---|---|---|
| `fierce angry glare` | 눈썹 V자, 눈 부릅뜸, 이 악물기 | 격렬한 대립 | harsh underlighting, deep red | CU |
| `frustrated grimace` | 미간 잔주름, 입술 비틀림 | 반복된 실패 | flat harsh light | MCU |
| `cold resentful stare` | 눈 가늘게, 시선 고정, 입 꽉 다뭄 | 배신자를 바라봄 | cold side-light, low-key | CU |
| `suppressed rage expression` | 턱 긴장, 코 벌름, 표면은 평온 | 감정 억누르는 장면 | dramatic chiaroscuro | ECU |
| `contemptuous sneer` | 한쪽 입꼬리만 올라감, 고개 뒤로 | 무시, 우월감 | high-key cold light | CU |

#### 기쁨 계열

| 영문 키워드 | 얼굴 변화 | 감정 맥락 | 추천 조명 | 추천 샷 |
|---|---|---|---|---|
| `warmly smiling face` | 뒤셴 미소, 볼 올라감, 초승달 눈 | 진심 어린 행복 | warm golden ambient | MCU |
| `content serene expression` | 입꼬리 미세 올라감, 이완된 근육 | 평화, 안도 | soft natural daylight | CU |
| `euphoric expression` | 눈 크게+빛남, 입 크게, 눈물 맺힘 | 꿈이 이루어지는 순간 | bright rim light, golden flare | CU |
| `bittersweet smile` | 한쪽 입꼬리만, 눈 촉촉, 미간 살짝 | 슬프지만 웃음 | dusk light, amber+blue | CU |
| `shy bashful smile` | 시선 아래, 볼 붉어짐, 입술 깨묾 | 설렘, 첫 고백 | soft fill light, warm peach | MCU |

#### 놀람 · 공포 · 긴장 계열

| 영문 키워드 | 얼굴 변화 | 감정 맥락 | 추천 조명 | 추천 샷 |
|---|---|---|---|---|
| `surprised wide-eyed look` | 눈 크게, 눈썹 위로, 입 벌어짐 | 반전 | sudden sharp light | CU |
| `shocked expression` | 눈 최대 확장, 얼굴 창백 | 믿을 수 없는 사실 | cold overexposed flash | ECU |
| `fearful wide eyes` | 흰자 드러남, 입술 떨림 | 위협, 공포 | low-key underlighting | CU |
| `anxious nervous expression` | 눈 초점 불안정, 입술 누름 | 결과 기다림, 긴장 | fluorescent cool light | CU |
| `desperate pleading eyes` | 눈물 고임, 애원하는 시선 | 간청, 마지막 호소 | single spotlight, warm | ECU |

#### 그리움 · 중립 · 복합 계열

| 영문 키워드 | 얼굴 변화 | 감정 맥락 | 추천 조명 | 추천 샷 |
|---|---|---|---|---|
| `longing yearning gaze` | 먼 곳 응시, 고개 기울어짐 | 떠난 사람 생각 | warm backlight, fog | MCU |
| `tender loving gaze` | 눈 부드럽게, 입꼬리 미세 올라감 | 소중한 사람 바라봄 | soft warm two-point | CU |
| `empty vacant stare` | 초점 없음, 완전 이완 | 충격 후 멍함 | overcast flat, desaturated | CU |
| `steely-eyed determined look` | 눈 강하게 고정, 턱 올라감, 입 다뭄 | 각오, 복수 | dramatic key, high contrast | MCU |
| `conflicted torn expression` | 눈썹 비대칭, 시선 흔들림 | 선택의 기로 | split two-color (warm/cool) | CU |
| `guilty ashamed face` | 시선 아래, 눈썹 안쪽 올라감 | 잘못 대면 | soft top-down, cool | CU |
| `exhausted hollow gaze` | 눈꺼풀 무겁게, 다크서클 | 번아웃 | cold blue-gray, low-key | MCU |

---

### 1.2 포즈(Body Pose)

> S3 `character_direction.pose`와 S4 `[SUBJECT]` 블록에 삽입

#### 서 있는 포즈

| 영문 키워드 | 체중/방향 | 감정 | 추천 샷 |
|---|---|---|---|
| `confident power stance` | 양발 어깨너비, 균등, 정면 | 자신감 | MS / FS |
| `casual weight-shifted stance` | 한쪽 다리 체중, 손 주머니 | 여유, 쿨함 | MS |
| `arms crossed standing` | 양팔 교차, 어깨 앞으로 | 방어적, 불신 | MS |
| `standing back turned to camera` | 등 카메라향, 고개 기울어짐 | 이별, 거절 | FS / LS |
| `standing head bowed low` | 목 구부러짐, 어깨 안으로 | 수치, 절망 | MS / FS |

#### 앉은 포즈

| 영문 키워드 | 체중/방향 | 감정 | 추천 샷 |
|---|---|---|---|
| `sitting on floor hugging knees` | 두 무릎 가슴으로, 몸 웅크림 | 극도의 슬픔, 절망 | MS / FS |
| `sitting on edge of surface` | 의자 끝 걸침, 팔꿈치 무릎 | 불안, 긴장된 대기 | MS |
| `slumped sitting collapsed` | 무너짐, 팔 축 늘어짐 | 탈진, 패배감 | MS / FS |
| `sitting with head in hands` | 두 손 얼굴 감춤 | 절망, 후회 | MCU |

#### 동적 포즈

| 영문 키워드 | 체중/방향 | 감정 | 추천 샷 |
|---|---|---|---|
| `walking away slowly` | 무게중심 앞, 등 카메라, 느린 발걸음 | 이별, 돌아오지 않음 | LS / FS |
| `running desperately forward` | 극앞 기울어짐, 팔 흔들림 | 절박함, 추격 | MS / LS |
| `reaching out one hand forward` | 팔 뻗음, 손바닥 펼침 | 간청, 이별 거부 | MS |
| `turning back to look over shoulder` | 상체 뒤로 비틀림 | 미련, 마지막 확인 | MS / FS |
| `collapsing to knees` | 무릎 바닥, 상체 앞 기울어짐 | 충격, 패배 | FS |

#### 기대는 · 누운 포즈

| 영문 키워드 | 체중/방향 | 감정 | 추천 샷 |
|---|---|---|---|
| `leaning forehead against window` | 이마 유리, 시선 밖 | 그리움, 고독 | CU / MS |
| `back against wall arms limp` | 등 벽, 미끄러지듯 | 탈력, 숨는 감정 | MS / FS |
| `lying in fetal position` | 옆으로 웅크림 | 극도의 슬픔, 자기보호 | MS / FS |
| `lying flat gazing at ceiling` | 등 바닥, 양팔 늘어짐 | 번아웃, 공허 | Top-down |

---

### 1.3 표정+포즈 프리셋 조합

| 조합명 | 프롬프트 (Copy-Paste) | 스토리 맥락 | 추천 샷 |
|---|---|---|---|
| 절망의 바닥 | `quietly weeping face, sitting on floor hugging knees` | 모든 것 잃은 순간 | MS |
| 이별의 뒷모습 | `melancholic gaze, walking away slowly` | 돌아서는 이별 | LS |
| 억눌린 각오 | `suppressed rage expression, rigid standing on guard` | 복수 결심 | MCU |
| 극한의 애원 | `desperate pleading eyes, collapsing to knees` | 마지막 간청 | FS |
| 침묵의 고독 | `solitary lonely expression, leaning forehead against window` | 빗속 그리움 | CU |
| 결전의 각오 | `steely-eyed determined look, confident power stance` | 영웅의 등장 | MS |
| 재회의 기쁨 | `euphoric expression, rushing forward arms wide` | 감동적 재회 | LS |
| 미련의 뒤돌아봄 | `wistful look, turning back to look over shoulder` | 떠나며 돌아봄 | MS |

---

## Part 2: SETTING & LIGHTING — 공간·배경·조명 키워드

### 2.1 배경/공간(SETTING) 키워드

> S3 `visual.background`와 S4 `[SETTING]` 블록에 삽입

#### 실내 공간

| 공간 | 핵심 오브젝트 (AI 인식률 높음) | 조명 (Day/Night) | 감정/장르 |
|---|---|---|---|
| Goshiwon | bunk bed, messy cables, instant noodle cup, cramped desk | Harsh fluorescent / Cyan PC glow | 고독, 빈곤, 스릴러 |
| Oktap-bang (Rooftop) | sliding glass door, laundry rack, DIY wooden table | Direct sunlight / Warm street lamp | 로맨스, 청춘 |
| Modern Apartment | marble floor, floor-to-ceiling window, pendant lights | Soft diffused / Warm LED strips | 재력, 가족 |
| Corner Cafe | wooden counter, Edison bulbs, steamed glass window, potted plants | Morning sun / Warm amber dim | 평화, 대화, 로맨스 |
| Industrial Bar | exposed brick, neon sign, liquor bottles, leather stools | Shadowy / Dim red/blue neon | 긴장, 범죄, 느와르 |
| Convenience Store | bright LED shelves, colorful cans, glass front | Overpowering cool white LED | 도시 외로움 |
| Hospital Room | IV drip stand, medical monitor, white curtains | Sterile cool white / Dim green night | 슬픔, 희망 |
| School Classroom | row of desks, green chalkboard, chalk dust | Bright side-window / Creepy moonlight | 청춘, 공포, 향수 |
| Subway Interior | stainless steel poles, grab handles, dark windows | Cool artificial white LED | 통근, 소외 |
| Noraebang | mirrored ball, neon laser, microphones, leather sofa | Dynamic RGB laser | 에너지, 혼돈, 청춘 |
1. 주거 및 개인 공간 (Residential: Living & Solitude)
공간/키워드,핵심 오브젝트 (AI 인식 최적화),기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Old Villa (Living Room),"Floral wallpaper, dark wooden floor, lace curtains, family photos, humidifiers",D: Soft window light / N: Warm flickering TV glow,"Family, Drama, Nostalgia","Old Korean villa living room, floral wallpaper, soft sunlight through lace curtains, lived-in feel."
Goshiwon (Tiny Room),"Bunk bed, plastic storage bins, messy cables, cup noodles, cramped desk",D: Harsh fluorescent / N: Cyan monitor glow,"Poverty, Solitude, Thriller","Cramped Goshiwon room, messy desk, cyan PC monitor glow, claustrophobic urban loneliness."
Modern Penthouse,"Marble floor, floor-to-ceiling windows, designer sofa, wine cellar, art pieces",D: Bright open sun / N: Indirect LED strip lights,"Wealth, Power, Revenge","Luxury penthouse, marble floors, panoramic city view at night, sophisticated indirect lighting."
Oktap-bang (Inside),"Sliding glass door, mismatched furniture, small fridge, floor mattress, string lights",D: Direct sun flare / N: Warm amber cozy lamp,"Youth, Romance, Dreams","Cozy rooftop room interior, sliding glass doors, warm sunset light, romantic youth aesthetic."
Attic (Storage),"Dust motes, old trunks, cobwebs, sloping ceiling, small round window","D: Single beam of light / N: Dark, moonlight only","Mystery, Childhood, Fantasy","Dusty attic, sloping ceiling, single beam of sunlight piercing darkness, mysterious old trunks."
2. 상업 및 여가 공간 (Commercial: Social & Public)
공간/키워드,핵심 오브젝트,기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Vintage Coffee Shop,"Wooden counter, LP records, Edison bulbs, steamed glass, leather chairs",D: Warm morning sun / N: Dim amber tungsten,"Romance, Peace, Retro","Vintage cafe, wooden counter, LP records on wall, Edison bulb glow, cozy nostalgic atmosphere."
Industrial Bar,"Exposed bricks, neon signs, liquor bottles, pool table, smoky haze","N: Red/Blue neon, high contrast","Noir, Crime, Tension","Gritty industrial bar, red neon sign, hazy smoke, liquor bottles, cinematic noir lighting."
Small Diner (Sikdang),"Metal tables, plastic stools, menu on wall, open kitchen, steam",D: Flat overhead light / N: Warm yellow bulbs,"Human Drama, Comedy","Small Korean diner, metal tables, steam from open kitchen, vibrant local life, warm lighting."
Old Bookstore,"Towering bookshelves, rolling ladder, yellowed paper, reading lamp",D: Soft dusty rays / N: Single desk lamp glow,"Wisdom, Mystery, Calm","Antique bookstore, floor-to-ceiling bookshelves, dust motes in sunbeams, quiet academic mood."
Noraebang (Karaoke),"Rotating disco ball, microphones, tambourines, neon laser lines",N: Dynamic RGB laser lights,"Chaos, Energy, Youth","Noraebang room, rotating disco ball, neon laser lights, microphones on table, dark purple glow."
3. 업무 및 공공 공간 (Professional: Work & Tension)
공간/키워드,핵심 오브젝트,기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Cramped Office,"Cubicles, stacks of paper, post-it notes, swivel chairs, coffee mugs",D: Cool white fluorescent / N: Single desk lamp,"Stress, Reality, Drama","Overcrowded office cubicle, stacks of paper, flickering fluorescent light, corporate stress."
Hospital Ward,"IV drip stand, medical monitor, white curtains, adjustable bed",D: Sterile soft white / N: Dim green night light,"Sadness, Hope, Human","Sterile hospital ward, IV drip stand, white curtains, soft morning light, emotional drama."
Art Studio,"Paint-splattered floor, canvases, easels, large windows, brushes",D: North-facing soft light / N: Low-key spotlight,"Passion, Artistic, Obsession","Messy art studio, paint-splattered floor, large windows, canvases, creative chaos, cinematic."
Police Station,"Whiteboard with photos, messy desks, handcuffs, water dispenser","N: Harsh overhead, blue/gray tint","Crime, Action, Suspense","Busy police station at night, whiteboard with suspect photos, harsh lighting, gritty atmosphere."
School Classroom,"Green chalkboard, wooden desks, chalk dust, backpack, hallway view",D: Side-window sunlight / N: Eerie moonlight,"Youth, Horror, Nostalgia","Empty classroom, green chalkboard, chalk dust in sunlight, nostalgic school drama aesthetic."
4. 교통 및 기타 공간 (Transport & Misc: Transition)
공간/키워드,핵심 오브젝트,기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Subway Interior,"Stainless steel poles, digital ads, yellow floor line, dark windows",N: Cool artificial LED,"Alienation, Commute","Modern subway car interior, stainless steel poles, motion blur outside windows, cold LED light."
Elevator Interior,"Mirrored walls, floor buttons, security camera, stainless steel",N: Harsh top-down spot,"Tension, Mystery, Thriller","Closed elevator interior, mirrored walls, harsh top-down light, cold metallic texture."
Old Stairwell,"Concrete steps, rusty handrail, flickering light, peeling paint","N: High contrast, long shadows","Crime, Horror, Chase","Dingy concrete stairwell, rusty handrail, flickering light, cinematic crime scene shadows."
Jimjilbang (Sauna),"Wood-paneled walls, floor mats, towels, water dispenser, stone fireplace",D: Warm amber glow / N: Low dim light,"Peace, Comedy, Daily","Korean sauna interior, wood-paneled walls, floor mats, warm cozy atmosphere, healing."
Underground Parking,"Concrete pillars, fluorescent tubes, puddles, security mirrors",N: Low-key green/gray tint,"Action, Crime, Fear","Grimy underground parking lot, concrete pillars, flickering fluorescent light, long shadows."
Gemini의 응답
프로덕션 디자이너의 시각으로 **실내 공간(Indoor Settings)**을 세부적으로 디벨롭했습니다. 한국 드라마와 영화의 미장센을 분석하여, 공간의 '생활감'과 '심리적 공기'를 AI가 완벽하게 재현하도록 설계한 마스터 리스트입니다.

1. 주거 및 개인 공간 (Residential: Living & Solitude)
공간/키워드	핵심 오브젝트 (AI 인식 최적화)	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Old Villa (Living Room)	Floral wallpaper, dark wooden floor, lace curtains, family photos, humidifiers	D: Soft window light / N: Warm flickering TV glow	Family, Drama, Nostalgia	Old Korean villa living room, floral wallpaper, soft sunlight through lace curtains, lived-in feel.
Goshiwon (Tiny Room)	Bunk bed, plastic storage bins, messy cables, cup noodles, cramped desk	D: Harsh fluorescent / N: Cyan monitor glow	Poverty, Solitude, Thriller	Cramped Goshiwon room, messy desk, cyan PC monitor glow, claustrophobic urban loneliness.
Modern Penthouse	Marble floor, floor-to-ceiling windows, designer sofa, wine cellar, art pieces	D: Bright open sun / N: Indirect LED strip lights	Wealth, Power, Revenge	Luxury penthouse, marble floors, panoramic city view at night, sophisticated indirect lighting.
Oktap-bang (Inside)	Sliding glass door, mismatched furniture, small fridge, floor mattress, string lights	D: Direct sun flare / N: Warm amber cozy lamp	Youth, Romance, Dreams	Cozy rooftop room interior, sliding glass doors, warm sunset light, romantic youth aesthetic.
Attic (Storage)	Dust motes, old trunks, cobwebs, sloping ceiling, small round window	D: Single beam of light / N: Dark, moonlight only	Mystery, Childhood, Fantasy	Dusty attic, sloping ceiling, single beam of sunlight piercing darkness, mysterious old trunks.
2. 상업 및 여가 공간 (Commercial: Social & Public)
공간/키워드	핵심 오브젝트	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Vintage Coffee Shop	Wooden counter, LP records, Edison bulbs, steamed glass, leather chairs	D: Warm morning sun / N: Dim amber tungsten	Romance, Peace, Retro	Vintage cafe, wooden counter, LP records on wall, Edison bulb glow, cozy nostalgic atmosphere.
Industrial Bar	Exposed bricks, neon signs, liquor bottles, pool table, smoky haze	N: Red/Blue neon, high contrast	Noir, Crime, Tension	Gritty industrial bar, red neon sign, hazy smoke, liquor bottles, cinematic noir lighting.
Small Diner (Sikdang)	Metal tables, plastic stools, menu on wall, open kitchen, steam	D: Flat overhead light / N: Warm yellow bulbs	Human Drama, Comedy	Small Korean diner, metal tables, steam from open kitchen, vibrant local life, warm lighting.
Old Bookstore	Towering bookshelves, rolling ladder, yellowed paper, reading lamp	D: Soft dusty rays / N: Single desk lamp glow	Wisdom, Mystery, Calm	Antique bookstore, floor-to-ceiling bookshelves, dust motes in sunbeams, quiet academic mood.
Noraebang (Karaoke)	Rotating disco ball, microphones, tambourines, neon laser lines	N: Dynamic RGB laser lights	Chaos, Energy, Youth	Noraebang room, rotating disco ball, neon laser lights, microphones on table, dark purple glow.
3. 업무 및 공공 공간 (Professional: Work & Tension)
공간/키워드	핵심 오브젝트	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Cramped Office	Cubicles, stacks of paper, post-it notes, swivel chairs, coffee mugs	D: Cool white fluorescent / N: Single desk lamp	Stress, Reality, Drama	Overcrowded office cubicle, stacks of paper, flickering fluorescent light, corporate stress.
Hospital Ward	IV drip stand, medical monitor, white curtains, adjustable bed	D: Sterile soft white / N: Dim green night light	Sadness, Hope, Human	Sterile hospital ward, IV drip stand, white curtains, soft morning light, emotional drama.
Art Studio	Paint-splattered floor, canvases, easels, large windows, brushes	D: North-facing soft light / N: Low-key spotlight	Passion, Artistic, Obsession	Messy art studio, paint-splattered floor, large windows, canvases, creative chaos, cinematic.
Police Station	Whiteboard with photos, messy desks, handcuffs, water dispenser	N: Harsh overhead, blue/gray tint	Crime, Action, Suspense	Busy police station at night, whiteboard with suspect photos, harsh lighting, gritty atmosphere.
School Classroom	Green chalkboard, wooden desks, chalk dust, backpack, hallway view	D: Side-window sunlight / N: Eerie moonlight	Youth, Horror, Nostalgia	Empty classroom, green chalkboard, chalk dust in sunlight, nostalgic school drama aesthetic.
4. 교통 및 기타 공간 (Transport & Misc: Transition)
공간/키워드	핵심 오브젝트	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Subway Interior	Stainless steel poles, digital ads, yellow floor line, dark windows	N: Cool artificial LED	Alienation, Commute	Modern subway car interior, stainless steel poles, motion blur outside windows, cold LED light.
Elevator Interior	Mirrored walls, floor buttons, security camera, stainless steel	N: Harsh top-down spot	Tension, Mystery, Thriller	Closed elevator interior, mirrored walls, harsh top-down light, cold metallic texture.
Old Stairwell	Concrete steps, rusty handrail, flickering light, peeling paint	N: High contrast, long shadows	Crime, Horror, Chase	Dingy concrete stairwell, rusty handrail, flickering light, cinematic crime scene shadows.
Jimjilbang (Sauna)	Wood-paneled walls, floor mats, towels, water dispenser, stone fireplace	D: Warm amber glow / N: Low dim light	Peace, Comedy, Daily	Korean sauna interior, wood-paneled walls, floor mats, warm cozy atmosphere, healing.
Underground Parking	Concrete pillars, fluorescent tubes, puddles, security mirrors	N: Low-key green/gray tint	Action, Crime, Fear	Grimy underground parking lot, concrete pillars, flickering fluorescent light, long shadows.
5. 실내 공간 디테일링 전략 (Interior Detail Enhancers)
실내 공간의 리얼리티를 극대화하는 '미술감독의 터치' 키워드입니다.

재질감 (Texture): Rough concrete, polished marble, worn wooden floor, stained carpet, peeling wallpaper.

공기감 (Atmosphere): Dust motes dancing in light, hazy smoke, steamed glass, volumetric fog, sterile smell (visualized by clean white).

생활감 (Lived-in): Cluttered, messy cables, unmade bed, half-empty coffee cup, stacks of books.

💡 미술감독의 팁:
실내 공간을 짤 때 **View through the window**를 추가해 보세요.

"View of city neon lights through the window" (도시의 화려함과 실내의 고독 대비)

"Rain streaks on the window pane" (멜로적 감성 극대화)

"Golden hour sun hitting the floor" (공간에 온기 부여)

#### 실외 공간

| 공간 | 핵심 오브젝트 | 날씨/계절 변형 | 감정/장르 |
|---|---|---|---|
| Narrow Alley | power lines, wet asphalt, brick walls, neon signs | Rainy (반사) / Foggy (미스터리) | 느와르, 범죄 |
| Crosswalk | traffic lights, white stripes, crowd | Rush hour / Midnight (empty) | 도시, 드라마 |
| Han River Bridge | steel girders, river ripples, city skyline | Blue Hour / Snowing | 로맨스, 멜랑콜리 |
| Bus Stop | glass shelter, route map, bench | Rainy (이별) / Autumn (낙엽) | 이별, 기다림 |
| Pine Forest | tall pines, mist, sunlight rays, moss | Foggy / Snow-capped | 판타지, 평화 |
| Public Playground | swings, sandpit, rubber floor | Golden Hour / Winter (eerie) | 유년, 공포 |
1. 도시 공간 (Urban Spaces: K-Noir & City Life)
공간/키워드,핵심 오브젝트 (AI 인식 최적화),기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Old Residential Alley,"Tangled power lines, stacked trash bags, green-painted gates, brick walls, steep stairs",D: High contrast shadows / N: Flickering sodium vapor lamp,"Noir, Poverty, Mystery","Narrow Seoul alley, tangled power lines, red brick walls, flickering orange streetlamp, gritty noir."
Main Boulevard,"Glass skyscrapers, digital billboards, traffic lights, bus lanes, street trees",D: Sharp direct sun / N: Vibrant neon & car light streaks,"Success, Urban, Action","Modern city boulevard, glass skyscrapers, neon billboard reflections, long exposure car light trails."
Pedestrian Underpass,"White tiled walls, fluorescent tubes, graffiti, echoey corridor, security camera","D: Cold artificial / N: Dim, green-tinted flickering light","Thriller, Crime, Solitude","Grimy pedestrian underpass, white tiled walls, flickering green fluorescent light, long lonely shadows."
Han River Park,"Steel bridge pillars, bicycle path, convenience store, river ripples, city skyline","D: Bright hazy sun / N: Cool blue twilight, bridge lights","Romance, Youth, Healing","Han River park at sunset, steel bridge structure, city skyline reflection on water, romantic golden hour."
Traditional Market,"Colorful tarps, wooden crates, hanging light bulbs, narrow paths, steam",D: Dappled light through tarps / N: Warm tungsten bulbs,"Human Drama, Comedy","Traditional Korean market, colorful tarps, steam from street food, warm hanging bulbs, vibrant life."
Industrial Complex,"Rusty pipes, shipping containers, concrete silos, wire fences, heavy machinery","D: Desaturated gray / N: Harsh floodlights, deep shadows","Action, Sci-fi, Gritty","Rusty industrial complex, shipping containers, cold metallic texture, harsh floodlights, cinematic grit."
2. 자연 공간 (Natural Landscapes: Cinematic Nature)
공간/키워드,핵심 오브젝트,기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Pine Forest Trail,"Tall pine trunks, pine needles on ground, mossy rocks, thick mist, sunbeams",D: Volumetric god rays / N: Pale moonlight through trees,"Fantasy, Mystery, Peace","Dense pine forest, volumetric god rays piercing mist, mossy ground, ethereal morning atmosphere."
Winter Beach,"Gray sand, crashing white waves, driftwood, lighthouse, seagulls","D: Overcast, cold blue / N: Pitch black, crashing white surf","Sadness, Loneliness, Art","Winter beach in overcast weather, cold gray waves, driftwood on sand, desolate melancholic mood."
Golden Reed Field,"Tall pampas grass, winding dirt path, mountains in distance, dragonflies","D: Back-lit golden hour / N: Silver moonlight, swaying grass","Nostalgia, Romance, Epic","Vast golden reed field at sunset, backlit pampas grass, warm amber glow, nostalgic cinematic vista."
Rocky Mountain Peak,"Jagged cliffs, stunted pine trees, sea of clouds, distant peaks, sunrise","D: Epic sunrise, orange-purple / N: Deep starlit sky, Milky Way","Grandeur, Adventure, Epic","Majestic mountain peak above clouds, jagged rocks, epic sunrise glow, 8k cinematic landscape."
Quiet Riverside,"Willow trees, river mist, pebbles, wooden pier, reflection of moon","D: Soft morning haze / N: Pale cool moonlight, ripples","Healing, Melodrama, Death","Quiet riverside at dawn, weeping willow trees, heavy river mist, soft ethereal lighting, peaceful."
Gemini의 응답
미술감독의 시각으로 **실외 공간(Outdoor Settings)**을 더욱 세밀하게 디벨롭했습니다. 한국적 도시 미학과 자연의 서사적 풍경을 결합하여, AI가 공간의 '공기'와 '질감'을 정확히 렌더링하도록 설계한 마스터 리스트입니다.

1. 도시 공간 (Urban Spaces: K-Noir & City Life)
공간/키워드	핵심 오브젝트 (AI 인식 최적화)	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Old Residential Alley	Tangled power lines, stacked trash bags, green-painted gates, brick walls, steep stairs	D: High contrast shadows / N: Flickering sodium vapor lamp	Noir, Poverty, Mystery	Narrow Seoul alley, tangled power lines, red brick walls, flickering orange streetlamp, gritty noir.
Main Boulevard	Glass skyscrapers, digital billboards, traffic lights, bus lanes, street trees	D: Sharp direct sun / N: Vibrant neon & car light streaks	Success, Urban, Action	Modern city boulevard, glass skyscrapers, neon billboard reflections, long exposure car light trails.
Pedestrian Underpass	White tiled walls, fluorescent tubes, graffiti, echoey corridor, security camera	D: Cold artificial / N: Dim, green-tinted flickering light	Thriller, Crime, Solitude	Grimy pedestrian underpass, white tiled walls, flickering green fluorescent light, long lonely shadows.
Han River Park	Steel bridge pillars, bicycle path, convenience store, river ripples, city skyline	D: Bright hazy sun / N: Cool blue twilight, bridge lights	Romance, Youth, Healing	Han River park at sunset, steel bridge structure, city skyline reflection on water, romantic golden hour.
Traditional Market	Colorful tarps, wooden crates, hanging light bulbs, narrow paths, steam	D: Dappled light through tarps / N: Warm tungsten bulbs	Human Drama, Comedy	Traditional Korean market, colorful tarps, steam from street food, warm hanging bulbs, vibrant life.
Industrial Complex	Rusty pipes, shipping containers, concrete silos, wire fences, heavy machinery	D: Desaturated gray / N: Harsh floodlights, deep shadows	Action, Sci-fi, Gritty	Rusty industrial complex, shipping containers, cold metallic texture, harsh floodlights, cinematic grit.
2. 자연 공간 (Natural Landscapes: Cinematic Nature)
공간/키워드	핵심 오브젝트	기본 조명 (Day/Night)	감정/장르	프롬프트 예문 (1줄)
Pine Forest Trail	Tall pine trunks, pine needles on ground, mossy rocks, thick mist, sunbeams	D: Volumetric god rays / N: Pale moonlight through trees	Fantasy, Mystery, Peace	Dense pine forest, volumetric god rays piercing mist, mossy ground, ethereal morning atmosphere.
Winter Beach	Gray sand, crashing white waves, driftwood, lighthouse, seagulls	D: Overcast, cold blue / N: Pitch black, crashing white surf	Sadness, Loneliness, Art	Winter beach in overcast weather, cold gray waves, driftwood on sand, desolate melancholic mood.
Golden Reed Field	Tall pampas grass, winding dirt path, mountains in distance, dragonflies	D: Back-lit golden hour / N: Silver moonlight, swaying grass	Nostalgia, Romance, Epic	Vast golden reed field at sunset, backlit pampas grass, warm amber glow, nostalgic cinematic vista.
Rocky Mountain Peak	Jagged cliffs, stunted pine trees, sea of clouds, distant peaks, sunrise	D: Epic sunrise, orange-purple / N: Deep starlit sky, Milky Way	Grandeur, Adventure, Epic	Majestic mountain peak above clouds, jagged rocks, epic sunrise glow, 8k cinematic landscape.
Quiet Riverside	Willow trees, river mist, pebbles, wooden pier, reflection of moon	D: Soft morning haze / N: Pale cool moonlight, ripples	Healing, Melodrama, Death	Quiet riverside at dawn, weeping willow trees, heavy river mist, soft ethereal lighting, peaceful.
3. 전환/공공 공간 (Public & Transition Spaces)
공간/키워드,핵심 오브젝트,기본 조명 (Day/Night),감정/장르,프롬프트 예문 (1줄)
Empty Playground,"Rusty swings, colorful slide, sandpit, rubber floor, apartment background",D: Long afternoon shadows / N: Single eerie streetlamp,"Horror, Childhood, Mystery","Deserted playground at night, rusty swings swaying, eerie green streetlamp, deep shadows."
Abandoned Parking Lot,"Cracked asphalt, faded yellow lines, puddles, overgrown weeds, rusty signs","D: Harsh, flat sun / N: Sodium vapor orange, shadows","Crime, Thriller, Action","Abandoned parking lot, cracked asphalt with puddles, rusty fences, orange sodium vapor light, noir."
School Rooftop,"Green waterproof floor, water tank, rusted railings, city view, blue sky","D: Bright open sky / N: City lights, cool night air","Youth, Melancholy, Romance","School rooftop, green floor paint, rusty railing, wide city view at sunset, youth drama aesthetic."
Bus Stop (Rainy),"Glass shelter, glowing ad board, bench, wet road, reflections",D: Muted gray light / N: Neon reflections on wet asphalt,"Waiting, Parting, Urban","Lonely bus stop in heavy rain, glowing glass shelter, neon reflections on wet road, blue hour."
Construction Site,"Scaffolding, blue mesh, cranes, concrete dust, orange cones","D: High-key, dusty / N: High-intensity work lights","Action, Suspense, Industry","Construction site at night, towering cranes, blue safety mesh, harsh work lights, cinematic action."
4. 날씨 및 계절별 환경 디벨롭 (Weather & Season Variations)
공간의 분위기를 한순간에 바꾸는 '환경 텍스처' 키워드입니다.

[Spring] Cherry Blossom Blizzard: swirling pink petals, soft pastel lighting, spring breeze, romantic glow.

[Summer] Monsoon Heat: wet asphalt steam, heavy rain streaks, saturated greens, oppressive humidity.

[Autumn] Dried Leaves: crunchy brown leaves, deep orange palette, low-angle golden sun, crisp air.

[Winter] Frost & Ice: frost on metal, frozen puddles, white breath, pale blue desaturated tint.

[Stormy] Gale Wind: flying debris, swaying trees, dark turbulent sky, lightning flashes, motion blur.

[Foggy] Low Visibility: volumetric fog, hidden silhouettes, muffled light, mysterious depth.
1. 세부 기상 상태 (Weather Detail)
기상은 화면의 **'텍스처'**와 **'빛의 투과율'**을 결정합니다.
기상 유형,시각적 특성 (미술 포인트),감정적 효과,AI 핵심 프롬프트 키워드
Drizzle (이슬비),"미세한 물안개, 옷 표면의 이슬, 은은한 광택","차분함, 나른함, 서정적","soft drizzle, mist, dew on skin, muted colors"
Torrential Rain,"강한 빗줄기(Streaks), 물웅덩이 튀김, 낮은 가시성","갈등, 폭발, 비극, 느와르","heavy rain, torrential, water splashes, wet asphalt reflections"
Dense Fog,"볼륨감 있는 안개, 실루엣 강조, 빛의 번짐","미스테리, 고립, 불확실성","thick fog, volumetric haze, hidden silhouettes, muffled light"
Heat Haze (지열),"아지랑이, 배경의 일렁임, 건조한 질감","갈등의 고조, 여름의 열기","heat haze, shimmering air, desert heat, distorted background"
Overcast (흐림),"그림자 없는 부드러운 빛, 낮은 채도, 평평한 명암","우울, 진지함, 객관성","overcast sky, flat lighting, gloomy, desaturated tones"
Lightning Storm,"순간적인 강한 섬광, 먹구름, 높은 명암 대비","공포, 위기, 초자연적","lightning flash, dark turbulent clouds, high contrast, dramatic"
Dust Storm,"주황빛 대기, 거친 입자감, 태양 가림","포스트 아포칼립스, 혹독함","dust storm, sepia tint, sand particles, low visibility"
2. 계절별 미장센 (Seasonal Mise-en-scène)
계절은 공간의 **'색채 팔레트'**와 **'온도감'**을 규정합니다.

🌸 봄 (Spring: Rebirth & Softness)
Early Spring: Pale green buds, melting ice, crisp but soft morning air.

Cherry Blossom Blizzard: Swirling pink petals (Komorebi), soft pastel palette, romantic haze.

Spring Haze: Dusty but warm sunbeams, yellow pollen motes, nostalgic mood.

🌿 여름 (Summer: Vitality & Humidity)
Lush Greenery: Deep emerald leaves, high saturation, vibrant life, dappled sunlight.

Monsoon Humidity: Steaming wet roads, oppressive dark clouds, sweating skin, heavy air.

Summer Night: Blue-tinted darkness, glowing fireflies, distant lightning, neon reflections.

🍂 가을 (Autumn: Decay & Gold)
Late Autumn: Deep amber and rust colors, crunchy dried leaves, low-angle golden sun.

Crisp Morning: White frost on grass, clear blue sky, long sharp shadows, lonely vibe.

Harvest Dusk: Deep purple and orange sky, silhouetted trees, harvest moon.

❄️ 겨울 (Winter: Purity & Desolation)
Blizzard: White-out conditions, swirling snow, frozen textures, harsh wind blur.

Clear Cold: Pale blue tint, icy breath, long blue shadows, crystalline clarity.

Thawing Winter: Dirty slush on ground, dripping icicles, gray sky, bleak atmosphere.
3. 환경 효과 레이어 (Environmental Layers)
공간에 생동감을 더하는 '대기 입자' 설정입니다.
키워드,물리적 묘사,서사적 기능,프롬프트 삽입 형태
Tyndall Effect,먼지나 안개 사이로 비치는 뚜렷한 빛줄기,"신성함, 희망, 발견","volumetric god rays, Tyndall effect"
Wet Surfaces,모든 표면이 젖어 빛을 반사함,"도시적 세련미, 비극적 아름다움","wet reflections, glossy surfaces, rain-soaked"
Frost & Ice,사물 외곽의 하얀 서리나 얼음 결정,"가혹함, 정지된 시간","frost-covered, icy texture, frozen edges"
Swirling Petals/Leaves,바람에 날리는 꽃잎이나 낙엽,"시간의 흐름, 감정의 동요","flying petals, swirling leaves, wind motion"
Hazy Bloom,빛이 번져서 경계가 모호해지는 현상,"꿈, 환각, 과거 회상","soft bloom, hazy glow, ethereal diffusion"
4. 날씨/계절별 프롬프트 레시피 (Recipes)
[장르: 멜로] 비 오는 날의 편의점:

Interior view through a wet window, Korean convenience store, heavy rain streaks on glass, neon reflections, soft warm indoor light vs cold blue rainy exterior, cinematic drama.

[장르: 청춘] 여름날의 학교 복도:

Sunny school hallway, lush green trees outside, dappled sunlight (Komorebi), heat haze, high saturation, floating dust motes, nostalgic youth atmosphere.

[장르: 스릴러] 안개 낀 새벽의 산길:

Dense fog on a mountain trail, blue hour, low visibility, towering pine silhouettes, volumetric haze, eerie silence, cinematic mystery, dark cool tones.
💡 전문가의 팁:
AI 이미지 생성 시 날씨 효과를 극대화하려면 Lens Surface 상태를 프롬프트에 추가해 보세요.

Water droplets on camera lens (현장감 극대화)

Foggy lens filter (몽환적 효과)

Lens flare from harsh sun (여름의 뜨거움)
5. 실외 공간용 소품(Props) 및 배치 전략
공간 유형,추천 소품 (AI 인식 최적화),배치 (전경/배경),서사적 기능
도시 골목,"버려진 우산, 길고양이, 구겨진 전단지",전경(Close-up),"생활감, 고독감 강조"
공사장/폐허,"깨진 유리 파편, 펄럭이는 비닐, 경고 테이프",중경(Midground),"위험, 미스테리 암시"
자연(숲/강),"낀 이끼, 물안개, 마른 나뭇가지",전경(Detail),"시간의 흐름, 신비로움"
학교/놀이터,"주인 없는 신발, 굴러다니는 공, 녹슨 체인",중경(Midground),"상실감, 과거의 흔적"
💡 미술감독의 팁:
실외 공간을 프롬프트로 짤 때 **Ground Texture**를 명시해 보세요.

"Wet asphalt with puddles" (비 온 뒤 도시)

"Cracked concrete with weeds" (쇠락한 공간)

"Dry fallen leaves" (가을의 정서)
이 작은 디테일이 공간의 '시네마틱한 리얼리티'를 완성합니다.

#### 시간대별 환경

| 시간대 | 하늘 색 | 그림자 | 프롬프트 키워드 |
|---|---|---|---|
| Dawn (4-6시) | pale indigo, misty white | faint, elongated | `pre-dawn, misty indigo sky, soft ambient` |
| Morning (7-9시) | pale blue, crisp yellow | sharp, medium | `early morning sun, crisp clarity, long soft shadows` |
| Afternoon (1-4시) | deep blue, white clouds | short, harsh | `harsh midday sun, high contrast, vertical shadows` |
| Golden Hour (5-6시) | orange, amber, pink | extremely long, soft | `golden hour, warm amber glow, long dramatic shadows` |
| Blue Hour (6-7시) | deep cobalt, violet | shadowless, diffused | `blue hour, twilight sky, cobalt tint, city lights` |
| Night (8-11시) | pitch black, navy edges | multiple artificial | `nighttime, artificial lighting, deep shadows` |
| Midnight (12-3시) | deep void, moonlight | single hard (moon) | `midnight, moonlit, pitch black background` |

#### 날씨/계절

| 날씨 | 시각적 특성 | 감정 | 프롬프트 키워드 |
|---|---|---|---|
| Heavy Rain | wet reflections, splashes, hazy distance | 슬픔, 느와르 | `heavy rain, wet reflections, water droplets` |
| Heavy Fog | volumetric depth, muted colors | 미스터리, 공포 | `thick fog, misty, volumetric haze` |
| Cherry Blossom | pink petals, soft pink tint | 첫사랑, 봄 | `cherry blossom petals falling, spring` |
| Summer Lush | vibrant green, harsh sun | 활력, 청춘 | `lush greenery, high saturation, summer` |
| Winter Snow | white blanket, frosty breath, icy texture | 순수, 외로움 | `snow-covered, frozen, frosty breath` |

#### 소품 라이브러리 (장면 특화)

| 장면 유형 | 소품 (프롬프트 키워드) | 배치 | 서사적 기능 |
|---|---|---|---|
| 이별 | 젖은 티슈, 버려진 반지케이스, 차가운 커피, 구겨진 편지 | 전경(CU) | 상실감 암시 |
| 고백 | 작은 꽃다발, 일렁이는 촛불, 김 나는 머그컵 | 중경 | 설렘, 온기 |
| 추격 | 뒤집힌 쓰레기통, 깨진 유리, 흩날리는 전단지 | 배경 | 긴박함 |
| 회상 | 카세트 테이프, 먼지 쌓인 인형, 빛바랜 사진 | 전경(Macro) | 향수 |
| 사무실 | 포스트잇 모니터, 식은 커피, 쌓인 서류 | 전경/중경 | 피로, 일의 무게 |
| 병원 | 반쯤 열린 커튼, 알약 팩, 접이식 의자 | 배경/중경 | 기다림의 고통 |
| 일상 | 장바구니, 열쇠, 충전 중인 폰, 슬리퍼 | 전경/중경 | 캐릭터의 평범성 |

---

### 2.2 조명(LIGHTING) 키워드

> S3 `visual.lighting`과 S4 `[LIGHTING]` 블록에 삽입

#### 조명 방향/패턴

| 영문 키워드 | 기술 묘사 | 감정 효과 | 추천 장면 |
|---|---|---|---|
| Front-lit | 정면 투사, 그림자 거의 없음 | 정직함, 순수 | 뷰티 CU |
| Back-lit | 역광, 테두리 강조 | 신비, 영웅적 | 실루엣, 일몰 |
| Side-lit | 90° 측면, 극단적 명암 | 고뇌, 질감 강조 | 흑백, 인물 |
| Rembrandt lighting | 45° 측면, 삼각형 빛 | 클래식, 권위 | 초상화, 시대극 |
| Butterfly lighting | 카메라 위쪽 정면 | 우아함, 여성미 | 패션, Paramount |
| Split lighting | 정측면 90° | 이중성, 갈등 | 스릴러, 악역 |
| Rim light | 뒤 대각선, 외곽선 | 존재감 부각 | 야간 액션 |
| Top-lit | 수직 위, 눈 그림자 깊음 | 압박, 신성함 | 심문실 |
| Under-lit | 아래, 비정상 그림자 | 공포, 악마적 | 호러 |
| Chiaroscuro | 강한 명암 대비 | 극적 긴장 | 르네상스풍 |

#### 색온도 (Kelvin)

| 영문 키워드 | K | 시간대/장소 | 감정 |
|---|---|---|---|
| Candlelight amber | 2000K | 촛불 아래 | 친밀, 고전 로맨스 |
| Warm amber tungsten | 3000K | 실내 전구, 밤 거실 | 따뜻함, 안락 |
| Golden hour glow | 3500K | 일몰 직전 | 희망, 향수 |
| Late afternoon sun | 4500K | 오후 4~5시 | 나른함, 평화 |
| Highnoon daylight | 5500K | 정오 | 중립, 활기 |
| Overcast gray | 6500K | 흐린 날 | 우울, 진지 |
| Cool daylight blue | 7500K | 그늘, 이른 아침 | 고독, 냉정 |
| Blue hour atmosphere | 8500K | 일몰 후 잔광 | 몽환, 도시적 우울 |
| Deep dusk blue | 10000K | 깊은 밤, 설원 | 혹독, 소외 |
| Neon magenta/cyan | N/A | 사이버펑크 도시 | 미래지향, 자극 |

#### 특수 조명 효과

| 영문 키워드 | 발생 조건 | 감정 효과 | 프롬프트 팁 |
|---|---|---|---|
| Lens flare | 광원이 렌즈 향할 때 | 드라마틱 | anamorphic flare |
| God rays | 먼지/안개+강한 빛 | 신성, 경외 | crepuscular rays |
| Bokeh light orbs | 초점 흐린 배경 광원 | 낭만, 몽환 | f/1.8 aperture |
| Volumetric fog | 공기 중 입자 | 입체 공간감, 미스터리 | haze, misty |
| Dappled light | 나뭇잎 통과 | 평화, 자연미 | leaf shadows, komorebi |
| Silhouette | 배경 > 피사체 밝기 | 익명, 고독 | 피사체 디테일 제거 |

#### 감정별 조명 레시피

| 감정 | 광원 방향 | 색온도 | 특수효과 | 프롬프트 1줄 |
|---|---|---|---|---|
| 로맨스 | Side/Back | 2500K | Bokeh, Golden hour | `Side-lit, 2500K golden hour, soft bokeh, film grain` |
| 슬픔/고독 | Side-lit | 7000K | Window light, Haze | `Cold side-lighting, 7000K blue hour, volumetric haze` |
| 긴장/서스펜스 | Split | 4000K | Chiaroscuro | `Split-lighting, harsh chiaroscuro, 4000K` |
| 희망/새 시작 | Back-lit | 5500K | God rays, Lens flare | `Back-lighting, 5500K, god rays, lens flare` |
| 분노/갈등 | Under-lit | 3000K | High contrast, Fire | `Under-lit, 3000K fiery orange, high contrast` |
| 몽환/꿈 | Top-lit | 8000K | Bloom, Pastel | `Ethereal top-lit, 8000K pastel blue, bloom` |
| 공포/불안 | Under-lit | 6000K | Flickering | `Under-lighting, 6000K cold pale, flickering` |
| 평화/안정 | Loop | 3500K | Dappled light | `Loop-lighting, 3500K amber, dappled sunlight` |

---

## Part 3: CAMERA & STYLE — 카메라·구도·스타일·부정어

### 3.1 카메라 & 구도

> S3 `visual` 섹션과 S4 `[CAMERA]` 블록에 삽입

#### 샷 사이즈

| 약어 | 영문 키워드 | 프레임 범위 | 감정 효과 | 서사적 기능 |
|---|---|---|---|---|
| ELS | `extreme long shot, wide vista` | 인물 아주 작게+배경 압도 | 고립, 경외 | 세계관 제시 |
| LS | `full body shot, environment focus` | 전신+환경 | 위치 정보 | 관계 정립 |
| MLS | `medium long shot, knee-up` | 무릎 위 | 행동 준비 | 액션 강조 |
| MS | `medium shot, waist-up` | 허리 위 | 안정, 대화 | 상호작용 |
| MCU | `medium close-up, chest-up` | 가슴 위 | 친밀, 몰입 | 감정 전조 |
| CU | `close-up shot, portrait` | 얼굴 전체 | 강렬한 감정 | 내면 노출 |
| BCU | `big close-up, face focus` | 이마~턱 | 압박, 긴장 | 진실 확인 |
| ECU | `macro shot, eye close-up` | 눈/입 등 부분 | 관찰, 상징 | 디테일 의미 |

#### 카메라 앵글

| 영문 키워드 | 심리적 효과 | 프롬프트 삽입 |
|---|---|---|
| Eye-level | 객관, 안정, 신뢰 | `eye-level angle, neutral view` |
| Low-angle | 권위, 영웅적 | `low-angle shot, looking up` |
| High-angle | 취약, 무력 | `high-angle shot, looking down` |
| Bird's-eye | 초월적 시선 | `bird's eye view, top-down` |
| Dutch/Canted | 혼란, 불안 | `dutch angle, tilted frame` |
| Over-the-shoulder | 대결, 연결 | `over-the-shoulder shot (OTS)` |
| POV | 일체감, 긴박 | `POV shot, first-person view` |

#### 카메라 무브먼트 (정지 이미지 암시 기법)

| 영문 키워드 | 서사적 기능 | AI 암시 기법 | 프롬프트 |
|---|---|---|---|
| Static | 관조적, 정적 | 완벽한 좌우 대칭, 선명도 | `static shot, still camera` |
| Dolly in | 발견 | 원근감 왜곡, 모션 블러 | `dolly in, forward motion` |
| Tracking shot | 긴박감 | 피사체 선명+배경 이동 | `tracking shot, action follow` |
| Handheld | 사실주의, 긴장 | 불규칙 각도, 거친 질감 | `handheld cam, shaky camera` |
| Rack focus | 시선 강제 이동 | 한쪽 보케+한쪽 선명 | `rack focus, selective focus` |

#### 구도 원칙

| 영문 키워드 | 감정 효과 | 추천 장면 | 프롬프트 |
|---|---|---|---|
| Rule of thirds | 안정, 자연스러운 여백 | 야외 인물, 풍경 | `rule of thirds, off-center` |
| Center frame | 강력한 존재감 | 리더 등장 | `centered composition` |
| Symmetry | 질서, 신성함 | 건축물 | `symmetrical, mirror image` |
| Leading lines | 깊이감, 목표 강조 | 복도, 길 | `leading lines, perspective` |
| Frame within frame | 갇힌 느낌, 관음 | 비밀 엿보기 | `frame within a frame` |
| Negative space | 외로움, 무한함 | 사막 위 인물 | `minimalist, negative space` |
| Depth layering | 공간감, 레이어링 | 군중 속 주인공 | `foreground, 3D depth` |

#### 피사계 심도(DOF) & 렌즈 화각

| 구분 | 프롬프트 키워드 | 효과 |
|---|---|---|
| f/1.4~2.8 | `ultra-shallow depth of field, bokeh` | 배경 완전 날림, 감정 몰입 |
| f/4~5.6 | `soft background` | 배경 어느 정도 보임 |
| f/8~16 | `deep focus, sharp background` | 전체 선명, 대서사시 |
| 24mm 광각 | `wide angle lens, 24mm` | 공간 왜곡, 광활 |
| 50mm 표준 | `50mm lens, natural view` | 자연스러운 시야 |
| 85mm 중망원 | `85mm, portrait lens` | 인물 피부 최적, 배경 압축 |
| 135mm+ 망원 | `telephoto lens, 200mm` | 극단적 배경 압축, 감시 느낌 |

---

### 3.2 스타일 프리셋 & 부정 프롬프트

> S4 `[STYLE]`과 `[NEGATIVE]` 블록에 삽입

#### 스타일 프리셋

| 프리셋 ID | 프롬프트 문자열 | 장르 | CFG / Steps / Sampler |
|---|---|---|---|
| photorealistic-cinematic | `Cinematic K-drama aesthetic, soft clean lighting, high-end DI color grading, 85mm lens, shallow DOF, clear skin texture, subtle warm highlights` | 로맨스, 현대극 | 4.5~6 / 30 / DPM++ 2M Karras |
| photorealistic-documentary | `Raw documentary film style, handheld motion blur, high ISO grain, natural available lighting, 35mm wide angle, muted natural colors` | 인디, 리얼리티 | 7 / 40 / Euler a |
| photorealistic-fashion | `High-fashion editorial, Vogue aesthetic, studio strobe, high contrast, glossy textures, 50mm prime, f/11` | 패션 화보 | 5 / 25 / Restart |
| korean-webtoon | `Modern Korean webtoon, clean line art, cel-shaded, vibrant digital coloring, manhwa, sparkling eyes` | 로판, 학원물 | 8 / 28 / DPM++ SDE |
| japanese-anime-cinematic | `Makoto Shinkai style, cinematic anime, detailed sky, lens flare, emotional lighting, 4k theatrical` | 판타지, 성장물 | 7 / 35 / DPM++ 2M Karras |
| noir-monochrome | `Classic film noir, 1940s, black and white, high contrast, Chiaroscuro, venetian blind shadows, 35mm grain` | 범죄, 미스터리 | 9 / 30 / Heun |
| retro-film-grain | `90s retro film, Fujifilm Superia 400, vintage color science, light leaks, heavy film grain, nostalgic` | 청춘물, 회상 | 6 / 30 / Euler |

#### 공통 부정어 (모든 스타일 적용)

```
worst quality, low quality, normal quality, watermark, text, signature, logo,
deformed, distorted, disfigured, extra fingers, mutated hands, fusion fingers,
blurry, out of focus
```

#### 장면 특화 부정어

| 장면 | 부정 프롬프트 키워드 |
|---|---|
| 실내 | `outdoor, trees, nature, sun, distorted furniture` |
| 실외 | `ceiling, indoor, wall, room, interior` |
| 야간 | `sunlight, daytime, bright sky, sun` |
| 비 | `dry ground, sunny, dust, desert` |
| 단체씬 | `merged bodies, duplicated people, missing limbs` |
| 공포 | `vibrant, cheerful, bright, sunny, pastel` |

#### 스타일 혼합 레시피

| 레시피 | 키워드 | 주의사항 |
|---|---|---|
| Nostalgic K-Drama | `(Cinematic K-drama:1.2), (90s retro film grain:0.8), soft warm lighting, Fujifilm colors` | film grain 수치 조절 |
| Cyberpunk Noir | `(Film noir chiaroscuro:1.3), (Cyberpunk:0.7), monochrome + selective neon cyan/magenta` | 부정어에 `full color` 필수 |
| Artistic Anime | `(Theatrical anime:1.1), (Watercolor:0.9), paper texture, soft bleeding edges` | line art 두께 주의 |

> **2026 팁**: `masterpiece, 8k, best quality` 등 품질 부스터는 최신 모델(Flux, SD3.5)에서 효과 없음. 대신 `highly detailed skin pores, atmospheric perspective, ray tracing` 등 물리적 디테일 키워드 사용.

---

## Part 4: 장르별 시네마틱 연출 가이드

> S3 `visual`, `audio_direction`, `transition` 필드 작성 시 참조

### 4.1 장르별 연출 레시피

| 장르 | 카메라 패턴 | 선호 조명 | 편집 리듬 | 대표 전환 | 핵심 기법 TOP 3 |
|---|---|---|---|---|---|
| 로맨스/멜로 | Slow Dolly-in, Centric Orbit | Back-lit Golden Hour, Soft Diffusion | 감정 고조 시 6초+ 길게 | Soft Dissolve | Sparkle Catch-light, Extreme Shallow DOF, Slow Motion |
| 스릴러 | Creeping Pan, Dutch Angle | Chiaroscuro, High Contrast | 점점 짧아지는 Staccato | J-cut | Frame within Frame, Low-key (암부 70%), Cold Color Grading |
| 일상/힐링 | Static Shot 위주 | Natural Window Light | 보통 4~5초 | White Fade | Wide Vista, Komorebi, Depth Layering |
| 액션 | Handheld, Whip Pan | Hard Light (날카로운 하이라이트) | 1초 미만 Rapid-fire | Match-on-action | High Shutter Speed, POV 교차, Crash Zoom |
| 호러/공포 | Slow Dolly-in, Handheld Shake | Under-lighting | 긴 호흡 → 1프레임 삽입 | Smash Cut | Negative Space, Distorted Wide-angle, Flickering |
| 발라드 MV | Floating Steadicam | Side-lit Soft (눈물 입체) | 가사 소절 단위 | Cross-fade | Particulate in Light, Soft Focus, Environmental Metaphor |
| 댄스/팝 MV | Step Zoom, 360 Orbit | Strobe, RGB Neon | BPM 1/2 또는 1/4 박자 싱크 | Graphic Wipe | Centric Composition, Glow & Bloom, Speed Ramping |
| 몽환/판타지 | Crane up/down, 부유 | Top-lit Rim, Halo | 슬로우 템포 | Iris In/Out | Chromatic Aberration, Double Exposure, Prism |

### 4.2 감정 전환점(Pivot Point) 연출

| 전환 유형 | 카메라 | 조명 | 편집 | 프롬프트 힌트 |
|---|---|---|---|---|
| 행복→슬픔 | Eye-level → High-angle | Warm Gold → Cold Blue | Short → Long take | `shift from warm sun to blue shadow` |
| 평화→긴장 | Static → Handheld | Soft diff → Harsh contrast | Steady → Fast jump cuts | `unsettling vibration, deep shadows` |
| 혼란→깨달음 | Out of focus → Sharp | Dim/Haze → Clear sun | Erratic → Slow zoom-in | `clarity, sharp definition, light ray` |
| 분노→체념 | CU → ELS | Red/Hard → Desaturated | Fast → Extreme slow-mo | `pulling back to isolate person` |
| 현재→회상 | Sharp → Muted/Grainy | Present → Golden nostalgia | Hard cut → Dissolve | `film grain, sepia tone, hazy edges` |

### 4.3 BPM-컷 리듬 가이드

| BPM | 1박 길이 | 빠른 컷 (1박) | 보통 컷 (2~4박) | 느린 컷 (8박+) |
|---|---|---|---|---|
| 60 (발라드) | 1.0초 | 1.0초 | 2~4초 | 8초+ |
| 90 (미디엄) | 0.67초 | 0.67초 | 1.3~2.7초 | 5.3초+ |
| 120 (댄스) | 0.5초 | 0.5초 | 1~2초 | 4초+ |
| 150 (EDM) | 0.4초 | 0.4초 | 0.8~1.6초 | 3.2초+ |

---

## Part 5: SFX & 전환효과 키워드

> S3 `audio_direction.sfx`와 `transition` 필드에 삽입

### 5.1 전환효과(Transition) 사전

| 키워드 | 시각적 설명 | 서사적 기능 | 감정 전환 | 빈도 |
|---|---|---|---|---|
| CUT | 즉각적 교체 | 표준 진행 | 중립 | 상 |
| DISSOLVE | 두 화면 겹침 | 시간 경과, 몽환 | 그리움 | 중 |
| FADE IN/OUT | 검/흰에서 서서히 | 시작과 끝 | 탄생, 종결 | 상 |
| MATCH CUT | 형태 유사한 피사체 연결 | 시공간 초월 | 깨달음 | 하 |
| J-CUT | 소리 먼저 → 화면 전환 | 부드러운 예고 | 기대감 | 중 |
| L-CUT | 화면 바뀌어도 소리 유지 | 대화 연속, 여운 | 차분 | 중 |
| SMASH CUT | 갑작스러운 전환 | 충격, 반전 | 공포 | 중 |
| WHIP PAN | 빠른 휘두름 | 장소 급이동 | 긴박 | 중 |
| FLASHBACK | 화이트 아웃 → 과거 | 기억 소환 | 향수, 고통 | 상 |
| MONTAGE | 짧은 컷 연속 나열 | 정보 요약, 성장 | 성취감 | 중 |

### 5.2 SFX 키워드 — 카테고리별

#### 환경음/앰비언스

| 키워드 | 감정 | 장면 | Vol |
|---|---|---|---|
| Urban Traffic Hum | 도시 활기 | 대로, 횡단보도 | B |
| Subway Platform Chime | 한국적 일상 | 지하철역 | F |
| Convenience Store Bell | 익숙, 외로움 | 편의점 | F |
| Cafe Chatter & Clink | 편안, 북적임 | 카페 | B |
| Heavy Downpour | 우울, 고립 | 비 오는 밤 | B |
| Night Crickets | 평온, 고요 | 여름밤 야외 | B |
| Distant Police Siren | 불안 | 야간 골목 | S |

#### 행동 효과음 (Foley)

| 키워드 | 감정 | 장면 | Vol |
|---|---|---|---|
| Echoey Footsteps | 고독, 추격 | 빈 복도 | F |
| Door Creak & Slam | 단절, 공포 | 낡은 집 | F |
| Coffee Cup Clink | 여유, 대화 시작 | 대화 장면 | S |
| Phone Vibration on Table | 긴급, 불안 | 회의실 | F |
| Umbrella Snap Open | 비의 시작 | 비 오는 거리 | F |

#### 감정 강조 SFX

| 키워드 | 감정 | 장면 | Vol |
|---|---|---|---|
| Low Thumping Heartbeat | 극도의 긴장 | 위기 직전 | F |
| Fast Ticking Clock | 시간 압박 | 마감 | F |
| Sharp Tinnitus Ringing | 충격, 공황 | 사고 직후 | F |
| Glass Shattering | 파국, 결별 | 싸움 | F |
| Vacuum Silence | 감각 상실 | 폭발 직후 | F |
| Sub-bass Rumble | 초자연적 위협 | 재난 | B |

#### 음악적 SFX

| 키워드 | 감정 | 장면 | Vol |
|---|---|---|---|
| Reverse Cymbal Swell | 고조, 전환 직전 | 결정적 순간 | F |
| Deep Sub Drop | 충격의 무게감 | 반전 공개 | F |
| Piano Single Ping | 고독한 여운 | 회상 시작 | S |
| White Noise Riser | 에너지 폭발 상승 | 댄스 MV 전환 | B |
| Tape Stop Effect | 급중단, 유머 | 코미디, 당황 | F |

### 5.3 장면별 SFX 레시피 (레이어 조합)

| 장면 | 앰비언스(B) | 행동음(F) | 감정 SFX |
|---|---|---|---|
| 카페 대화 | Cafe Chatter + Espresso Hum | Coffee Cup Clink | Subtle Jazz (S) |
| 이별 빗속 | Heavy Downpour + Distant Traffic | Squelching footsteps | Vacuum Silence + Piano Ping |
| 추격 도심 | Urban Traffic + Siren | Heavy Breathing + Sprint | Heartbeat + String Stinger |
| 회상 과거 | Wind Howl (muted) | Film Projector Whir | Hazy Reverb + Echoed Voices |
| 고백 밤공원 | Night Crickets + City Hum | Rustling clothes | Synth Pad Swell + Heartbeat |
| 사무실 야근 | Air Conditioner Hum | Typing + Sipping cold coffee | Ticking Clock + Neon Buzz |
| 편의점 심야 | Fridge Motor Hum | Store Bell + Plastic bag | Distant Siren (S) |

---

## Part 6: 감독 스타일 레퍼런스

> S3 전체 톤 결정 시 선택적 참조

| 감독/스튜디오 | 시각적 시그니처 | 프롬프트 키워드 |
|---|---|---|
| 봉준호 | Deep focus, 계급 대비, 공간 레이어링 | `Bong Joon-ho style, deep focus, social realism, cluttered mise-en-scene` |
| 박찬욱 | 완벽 대칭, 강렬 원색, 바로크 느와르 | `Park Chan-wook aesthetic, extreme symmetry, vivid morbid color, baroque noir` |
| 이사강 | 시적 영상, 자연광, 몽환적 MV | `Lee Sa-gang style, poetic imagery, natural golden hour, dreamy soft focus` |
| 룸펜스 (Lumpens) | 서사적 스케일, 상징, 필름 그레인 | `Lumpens style, epic scale, symbolic objects, chiaroscuro, grainy film` |
| 디지페디 (Digipedi) | 대칭, 파스텔, 키치 초현실 | `Digipedi aesthetic, symmetry, pastel pop, flat lighting, quirky surrealism` |
| 리전드 필름 | 미래주의, 매크로, 네온 느와르 | `Rigend Film style, macro detail, neon cyan, glossy finish, futuristic noir` |

---

> **Vol 범례**: F = Foreground, B = Background, S = Subtle  
> **샷 약어**: ELS, LS, MLS, MS, MCU, CU, BCU, ECU (Part 3.1 참조)
