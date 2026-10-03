// --- Game State & Setup ---
const blocker = document.getElementById('blocker');
const instructions = document.getElementById('instructions');
const scoreVal = document.getElementById('score-val');

let scene, camera, renderer;
let clock = new THREE.Clock();

// Controls state
let isLocked = false;
let yaw = 0;
let pitch = 0;
const cameraDistance = 4.5;
const cameraHeightOffset = 1.6;
const cameraLookAtOffset = 1.0;

// Key state
const keys = { w: false, a: false, s: false, d: false, space: false };

// Player stats
const player = {
    mesh: null,
    width: 0.8,
    height: 1.8,
    position: new THREE.Vector3(0, 0.9, 0),
    velocity: new THREE.Vector3(),
    speed: 8,
    jumpForce: 9,
    gravity: 22,
    isGrounded: false
};

// Gun & Bullets
let gunMesh;
const bullets = [];
const bulletSpeed = 80;
const bulletLifeTime = 1.2;

// Enemy stats
const enemy = {
    meshGroup: null,
    position: new THREE.Vector3(0, 0.9, -18),
    isDead: false,
    deathTimer: 0,
    respawnTime: 2.5
};

let elims = 0;
let groundMesh;

// --- Building System State ---
let buildMode = 'none';
let previewMesh = null;
const GRID_SIZE = 3;
const placedStructures = [];

const slots = {
    none: document.getElementById('slot-weapon'),
    wall: document.getElementById('slot-wall'),
    floor: document.getElementById('slot-floor'),
    stair: document.getElementById('slot-stair')
};


// --- Pointer Lock API ---
instructions.addEventListener('click', () => {
    document.body.requestPointerLock();
});

document.addEventListener('pointerlockchange', () => {
    if (document.pointerLockElement === document.body) {
        isLocked = true;
        blocker.style.opacity = '0';
        setTimeout(() => { blocker.style.display = 'none'; }, 300);
    } else {
        isLocked = false;
        blocker.style.display = 'flex';
        setTimeout(() => { blocker.style.opacity = '1'; }, 10);
    }
});

// --- Input Handling ---
document.addEventListener('keydown', (e) => {
    switch (e.code) {
        case 'KeyW': keys.w = true; break;
        case 'KeyA': keys.a = true; break;
        case 'KeyS': keys.s = true; break;
        case 'KeyD': keys.d = true; break;
        case 'Space': keys.space = true; break;
        case 'KeyQ': toggleBuildMode('wall'); break;
        case 'KeyF': toggleBuildMode('floor'); break;
        case 'KeyG': toggleBuildMode('stair'); break;
    }
});

document.addEventListener('keyup', (e) => {
    switch (e.code) {
        case 'KeyW': keys.w = false; break;
        case 'KeyA': keys.a = false; break;
        case 'KeyS': keys.s = false; break;
        case 'KeyD': keys.d = false; break;
        case 'Space': keys.space = false; break;
    }
});

document.addEventListener('mousemove', (e) => {
    if (!isLocked) return;

    // マウス感度の調整
    const sensitivity = 0.002;
    yaw -= e.movementX * sensitivity;
    pitch -= e.movementY * sensitivity;

    // 上下の角度制限 (クランプ)
    pitch = Math.max(-Math.PI / 3.5, Math.min(Math.PI / 3.5, pitch));
});

document.addEventListener('mousedown', (e) => {
    if (!isLocked) return;
    if (e.button === 0) { // 左クリック
        if (buildMode === 'none') {
            fireBullet();
        } else {
            placeStructure();
        }
    }
});

// --- Building System Logic ---
function toggleBuildMode(mode) {
    if (buildMode === mode) {
        buildMode = 'none';
    } else {
        buildMode = mode;
    }

    // UIの active クラスを更新
    for (const key in slots) {
        if (slots[key]) {
            if (key === buildMode) {
                slots[key].classList.add('active');
            } else {
                slots[key].classList.remove('active');
            }
        }
    }

    updatePreviewMeshType();
}

function updatePreviewMeshType() {
    if (previewMesh) {
        scene.remove(previewMesh);
        previewMesh.traverse((child) => {
            if (child.isMesh) {
                child.geometry.dispose();
                child.material.dispose();
            }
        });
        previewMesh = null;
    }

    if (buildMode === 'none') return;

    previewMesh = new THREE.Group();

    const mat = new THREE.MeshBasicMaterial({
        color: 0x00fff2,
        transparent: true,
        opacity: 0.4,
        side: THREE.DoubleSide
    });

    let geom;
    if (buildMode === 'wall') {
        geom = new THREE.BoxGeometry(GRID_SIZE, GRID_SIZE, 0.15);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.y = GRID_SIZE / 2;
        previewMesh.add(mesh);
    } else if (buildMode === 'floor') {
        geom = new THREE.BoxGeometry(GRID_SIZE, 0.12, GRID_SIZE);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.y = 0.06;
        previewMesh.add(mesh);
    } else if (buildMode === 'stair') {
        geom = new THREE.BoxGeometry(GRID_SIZE, 0.15, GRID_SIZE * Math.SQRT2);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.rotation.x = -Math.PI / 4;
        mesh.position.set(0, GRID_SIZE / 2, 0);
        previewMesh.add(mesh);
    }

    scene.add(previewMesh);
}

function updatePreviewPosition() {
    if (!previewMesh || buildMode === 'none') return;

    const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw);
    const targetPos = player.position.clone().addScaledVector(forward, 3.5);

    let snapX = Math.round(targetPos.x / GRID_SIZE) * GRID_SIZE;
    let snapZ = Math.round(targetPos.z / GRID_SIZE) * GRID_SIZE;
    
    let snapY = Math.round((player.position.y - 0.9) / GRID_SIZE) * GRID_SIZE;
    if (snapY < 0) snapY = 0;

    const snappedYaw = Math.round(yaw / (Math.PI / 2)) * (Math.PI / 2);

    previewMesh.position.set(snapX, snapY, snapZ);
    
    if (buildMode === 'floor') {
        previewMesh.rotation.y = 0;
    } else {
        previewMesh.rotation.y = snappedYaw;
    }
}

function placeStructure() {
    if (!previewMesh || buildMode === 'none') return;

    const structGroup = new THREE.Group();
    let color = 0x5a189a; // 壁
    if (buildMode === 'floor') color = 0x3c096c; // 床
    if (buildMode === 'stair') color = 0x7b2cbf; // 階段

    const mat = new THREE.MeshStandardMaterial({
        color: color,
        roughness: 0.6,
        metalness: 0.2,
        side: THREE.DoubleSide
    });

    const wireframeMat = new THREE.MeshBasicMaterial({
        color: 0x00fff2,
        wireframe: true,
        transparent: true,
        opacity: 0.3
    });

    let geom;
    if (buildMode === 'wall') {
        geom = new THREE.BoxGeometry(GRID_SIZE, GRID_SIZE, 0.15);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.y = GRID_SIZE / 2;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        structGroup.add(mesh);

        const wf = new THREE.Mesh(geom, wireframeMat);
        wf.position.y = GRID_SIZE / 2;
        structGroup.add(wf);

        structGroup.userData = { type: 'wall' };
    } else if (buildMode === 'floor') {
        geom = new THREE.BoxGeometry(GRID_SIZE, 0.12, GRID_SIZE);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.y = 0.06;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        structGroup.add(mesh);

        const wf = new THREE.Mesh(geom, wireframeMat);
        wf.position.y = 0.06;
        structGroup.add(wf);

        structGroup.userData = { type: 'floor' };
    } else if (buildMode === 'stair') {
        geom = new THREE.BoxGeometry(GRID_SIZE, 0.15, GRID_SIZE * Math.SQRT2);
        const mesh = new THREE.Mesh(geom, mat);
        mesh.rotation.x = -Math.PI / 4;
        mesh.position.set(0, GRID_SIZE / 2, 0);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        structGroup.add(mesh);

        const wf = new THREE.Mesh(geom, wireframeMat);
        wf.rotation.x = -Math.PI / 4;
        wf.position.set(0, GRID_SIZE / 2, 0);
        structGroup.add(wf);

        structGroup.userData = { 
            type: 'stair',
            yaw: previewMesh.rotation.y
        };
    }

    structGroup.position.copy(previewMesh.position);
    structGroup.rotation.copy(previewMesh.rotation);

    scene.add(structGroup);
    placedStructures.push(structGroup);
}

function getPlayerBox(pos) {
    return new THREE.Box3(
        new THREE.Vector3(pos.x - 0.35, pos.y - 0.9, pos.z - 0.35),
        new THREE.Vector3(pos.x + 0.35, pos.y + 0.9, pos.z + 0.35)
    );
}

function resolveCollisions(axis, oldPos) {
    const pBox = getPlayerBox(player.position);

    for (const struct of placedStructures) {
        const type = struct.userData.type;

        if (type === 'wall' || type === 'floor') {
            const structBox = new THREE.Box3().setFromObject(struct);
            if (pBox.intersectsBox(structBox)) {
                if (axis === 'x') {
                    player.position.x = oldPos.x;
                } else if (axis === 'z') {
                    player.position.z = oldPos.z;
                } else if (axis === 'y') {
                    if (player.velocity.y <= 0) {
                        player.position.y = structBox.max.y + 0.9;
                        player.velocity.y = 0;
                        player.isGrounded = true;
                    } else {
                        player.position.y = structBox.min.y - 0.9;
                        player.velocity.y = 0;
                    }
                }
                pBox.copy(getPlayerBox(player.position));
            }
        } else if (type === 'stair') {
            const structBox = new THREE.Box3().setFromObject(struct);
            if (pBox.intersectsBox(structBox)) {
                const yaw = struct.userData.yaw;
                const relativePos = player.position.clone().sub(struct.position);
                relativePos.applyAxisAngle(new THREE.Vector3(0, 1, 0), -yaw);

                let localZ = relativePos.z;
                let t = (localZ + 1.5) / 3;
                t = Math.max(0, Math.min(1, t));
                const stairHeightAtPos = struct.position.y + (t * GRID_SIZE);

                const threshold = 0.8;
                if (player.position.y - 0.9 >= stairHeightAtPos - threshold && player.position.y - 0.9 <= stairHeightAtPos + 0.2) {
                    player.position.y = stairHeightAtPos + 0.9;
                    player.velocity.y = 0;
                    player.isGrounded = true;
                } else {
                    if (axis === 'x') player.position.x = oldPos.x;
                    if (axis === 'z') player.position.z = oldPos.z;
                    if (axis === 'y') {
                        if (player.velocity.y > 0 && player.position.y - 0.9 < struct.position.y) {
                            player.position.y = structBox.min.y - 0.9;
                            player.velocity.y = 0;
                        }
                    }
                }
                pBox.copy(getPlayerBox(player.position));
            }
        }
    }
}

// --- Initialize Game ---
function init() {
    // 1. Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0c0a1c);
    scene.fog = new THREE.FogExp2(0x0c0a1c, 0.015);

    // 2. Camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    // 3. Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // 4. Lights
    const ambientLight = new THREE.AmbientLight(0x4f3cc9, 0.4);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(20, 40, 20);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 100;
    const d = 30;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0005;
    scene.add(dirLight);

    // 追加の補助ライト（ネオン感の演出）
    const pointLight = new THREE.PointLight(0x00fff2, 0.8, 30);
    pointLight.position.set(0, 5, 0);
    scene.add(pointLight);

    // 5. Ground (3Dの地面)
    createGround();

    // 6. Player (三人称視点のプレイヤーモデル作成)
    createPlayer();

    // 7. Enemy (敵の作成)
    createEnemy();

    // Resize Event
    window.addEventListener('resize', onWindowResize);

    // Start Loop
    animate();
}

// 地面の作成
function createGround() {
    // 地面メッシュ
    const groundGeo = new THREE.PlaneGeometry(300, 300);
    const groundMat = new THREE.MeshStandardMaterial({
        color: 0x141226,
        roughness: 0.8,
        metalness: 0.2
    });
    groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // グリッドを重ねてサイバー感を出す
    const gridHelper = new THREE.GridHelper(300, 100, 0xff007f, 0x3d1b5c);
    gridHelper.position.y = 0.01; // 地面よりわずかに上
    scene.add(gridHelper);

    // 装飾用の障害物（立方体）をいくつか配置
    const boxGeo = new THREE.BoxGeometry(4, 4, 4);
    const boxMat = new THREE.MeshStandardMaterial({ color: 0x311066, roughness: 0.5 });
    
    for (let i = 0; i < 15; i++) {
        const box = new THREE.Mesh(boxGeo, boxMat);
        const angle = Math.random() * Math.PI * 2;
        const dist = 15 + Math.random() * 40;
        box.position.set(Math.sin(angle) * dist, 2, Math.cos(angle) * dist);
        box.castShadow = true;
        box.receiveShadow = true;
        box.userData = { type: 'wall' };
        scene.add(box);
        placedStructures.push(box);
    }
}

// プレイヤーキャラクターの作成（複数のパーツを組み合わせたSF風ロボット）
function createPlayer() {
    player.mesh = new THREE.Group();

    // 胴体 (Body - 青い角丸カプセル風)
    const bodyGeo = new THREE.CylinderGeometry(0.35, 0.35, 1.0, 16);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x240090, roughness: 0.3 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.6;
    body.castShadow = true;
    body.receiveShadow = true;
    player.mesh.add(body);

    // 頭部 (Head - 白い球体)
    const headGeo = new THREE.SphereGeometry(0.28, 16, 16);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.2 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 1.25;
    head.castShadow = true;
    player.mesh.add(head);

    // バイザー (Visor - 発光するシアンの目)
    const visorGeo = new THREE.BoxGeometry(0.35, 0.1, 0.15);
    const visorMat = new THREE.MeshBasicMaterial({ color: 0x00fff2 });
    const visor = new THREE.Mesh(visorGeo, visorMat);
    visor.position.set(0, 1.25, 0.22); // 正面に配置
    player.mesh.add(visor);

    // バックパック (Jetpack - 赤いシリンダー)
    const packGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.7, 8);
    const packMat = new THREE.MeshStandardMaterial({ color: 0xff0055 });
    const pack = new THREE.Mesh(packGeo, packMat);
    pack.position.set(0, 0.6, -0.4);
    pack.rotation.x = Math.PI / 12;
    pack.castShadow = true;
    player.mesh.add(pack);

    // 銃 (Gun)
    const gunGroup = new THREE.Group();
    const barrelGeo = new THREE.BoxGeometry(0.1, 0.1, 0.6);
    const barrelMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.8, roughness: 0.2 });
    const barrel = new THREE.Mesh(barrelGeo, barrelMat);
    barrel.position.set(0, 0, 0.2);
    barrel.castShadow = true;
    gunGroup.add(barrel);

    const gripGeo = new THREE.BoxGeometry(0.08, 0.2, 0.08);
    const grip = new THREE.Mesh(gripGeo, barrelMat);
    grip.position.set(0, -0.1, 0);
    gunGroup.add(grip);

    // 銃をプレイヤーの右側（右手付近）に配置
    gunGroup.position.set(0.45, 0.5, 0.2);
    player.mesh.add(gunGroup);
    gunMesh = gunGroup; // 弾丸発射位置の参照用

    // シーンに追加
    player.mesh.position.copy(player.position);
    scene.add(player.mesh);
}

// 敵キャラクターの作成（赤いホバー型ロボット）
function createEnemy() {
    enemy.meshGroup = new THREE.Group();

    // 敵胴体 (赤い直方体)
    const bodyGeo = new THREE.BoxGeometry(0.7, 0.8, 0.7);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xff0055, roughness: 0.4 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.6;
    body.castShadow = true;
    body.receiveShadow = true;
    enemy.meshGroup.add(body);

    // 敵頭部 (ダークグレーの球体)
    const headGeo = new THREE.SphereGeometry(0.25, 16, 16);
    const headMat = new THREE.MeshStandardMaterial({ color: 0x1f1f2e, roughness: 0.1 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 1.15;
    head.castShadow = true;
    enemy.meshGroup.add(head);

    // 敵の目 (発光する赤いシリンダー)
    const eyeGeo = new THREE.BoxGeometry(0.3, 0.08, 0.1);
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const eye = new THREE.Mesh(eyeGeo, eyeMat);
    eye.position.set(0, 1.15, 0.2);
    enemy.meshGroup.add(eye);

    // 敵下部のホバーノズル (シリンダー)
    const hoverGeo = new THREE.CylinderGeometry(0.2, 0.1, 0.3, 8);
    const hoverMat = new THREE.MeshStandardMaterial({ color: 0x3d3d3d, metalness: 0.7 });
    const hover = new THREE.Mesh(hoverGeo, hoverMat);
    hover.position.y = 0.1;
    enemy.meshGroup.add(hover);

    // ホバーエフェクト（ネオンブルーの輪）
    const ringGeo = new THREE.RingGeometry(0.25, 0.3, 16);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xff0055, side: THREE.DoubleSide });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = Math.PI / 2;
    ring.position.y = 0.02;
    enemy.meshGroup.add(ring);

    // シーンに追加
    enemy.meshGroup.position.copy(enemy.position);
    scene.add(enemy.meshGroup);
}

// 窓のリサイズ
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// --- Shoot Bullet ---
function fireBullet() {
    // カメラの正面方向を取得
    const dir = new THREE.Vector3();
    camera.getWorldDirection(dir);

    // 画面中央（照準）の目標点をレイキャストで求める
    const raycaster = new THREE.Raycaster();
    raycaster.set(camera.position, dir);

    // 当たり判定の対象
    const targets = [];
    enemy.meshGroup.traverse((child) => {
        if (child.isMesh) targets.push(child);
    });
    targets.push(groundMesh);

    // 建築物・障害物もレイキャストの対象に含める
    for (const struct of placedStructures) {
        struct.traverse((child) => {
            if (child.isMesh) targets.push(child);
        });
    }

    const intersects = raycaster.intersectObjects(targets);

    let targetPoint = new THREE.Vector3();
    if (intersects.length > 0) {
        targetPoint.copy(intersects[0].point);
    } else {
        // 何も当たらなかった場合は遠くを狙う
        targetPoint.copy(camera.position).addScaledVector(dir, 100);
    }

    // 発射位置（銃口のグローバル座標）
    const startPoint = new THREE.Vector3();
    if (gunMesh) {
        gunMesh.getWorldPosition(startPoint);
    } else {
        startPoint.copy(player.position).add(new THREE.Vector3(0, 0.6, 0.2));
    }

    // 発射方向
    const bulletDir = new THREE.Vector3().subVectors(targetPoint, startPoint).normalize();

    // 弾丸のメッシュ
    const bulletGeo = new THREE.SphereGeometry(0.12, 8, 8);
    const bulletMat = new THREE.MeshBasicMaterial({ color: 0x00fff2 });
    const bulletMesh = new THREE.Mesh(bulletGeo, bulletMat);
    bulletMesh.position.copy(startPoint);
    scene.add(bulletMesh);

    // 光源を弾に付ける（暗闇で弾が光るように）
    const bulletLight = new THREE.PointLight(0x00fff2, 1.0, 4);
    bulletMesh.add(bulletLight);

    bullets.push({
        mesh: bulletMesh,
        direction: bulletDir,
        life: bulletLifeTime
    });

    // 射撃反動風のアニメーション（銃を少し後ろに引く）
    if (gunMesh) {
        gunMesh.position.z = 0.05;
    }
}

// 弾の更新と当たり判定
function updateBullets(dt) {
    for (let i = bullets.length - 1; i >= 0; i--) {
        const b = bullets[i];
        b.life -= dt;

        if (b.life <= 0) {
            scene.remove(b.mesh);
            b.mesh.geometry.dispose();
            b.mesh.material.dispose();
            bullets.splice(i, 1);
            continue;
        }

        // 移動
        b.mesh.position.addScaledVector(b.direction, bulletSpeed * dt);

        // 敵との衝突判定
        if (!enemy.isDead && enemy.meshGroup) {
            const enemyBox = new THREE.Box3().setFromObject(enemy.meshGroup);
            const bulletPos = b.mesh.position;

            if (enemyBox.containsPoint(bulletPos)) {
                hitEnemy();

                // 弾の消去
                scene.remove(b.mesh);
                b.mesh.geometry.dispose();
                b.mesh.material.dispose();
                bullets.splice(i, 1);
                continue;
            }
        }

        // 建築物・障害物との衝突判定
        let hitStructure = false;
        for (const struct of placedStructures) {
            const structBox = new THREE.Box3().setFromObject(struct);
            if (structBox.containsPoint(b.mesh.position)) {
                scene.remove(b.mesh);
                b.mesh.geometry.dispose();
                b.mesh.material.dispose();
                bullets.splice(i, 1);
                hitStructure = true;
                break;
            }
        }
        if (hitStructure) continue;
    }
}

// 敵に弾が当たったときの処理
function hitEnemy() {
    enemy.isDead = true;
    enemy.deathTimer = enemy.respawnTime;

    // スコア加算
    elims += 1;
    scoreVal.innerText = elims;

    // 被弾時の火花エフェクト（簡易）
    const sparkGeo = new THREE.SphereGeometry(0.3, 8, 8);
    const sparkMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });
    const spark = new THREE.Mesh(sparkGeo, sparkMat);
    spark.position.copy(enemy.meshGroup.position).y += 0.6;
    scene.add(spark);
    setTimeout(() => {
        scene.remove(spark);
        sparkGeo.dispose();
        sparkMat.dispose();
    }, 150);
}

// 敵の更新
function updateEnemy(dt) {
    if (!enemy.meshGroup) return;

    if (enemy.isDead) {
        enemy.deathTimer -= dt;

        // 倒れるアニメーション（X軸方向に90度倒す）
        enemy.meshGroup.rotation.x = THREE.MathUtils.lerp(enemy.meshGroup.rotation.x, -Math.PI / 2, 8 * dt);
        // 地面に沈ませる
        enemy.meshGroup.position.y = THREE.MathUtils.lerp(enemy.meshGroup.position.y, 0.1, 4 * dt);

        if (enemy.deathTimer <= 0) {
            respawnEnemy();
        }
    } else {
        // 通常時: 少し上下に浮遊させる
        const time = clock.getElapsedTime();
        enemy.meshGroup.position.y = 0.9 + Math.sin(time * 3) * 0.08;
        
        // プレイヤーの方を常に向く（Y軸のみ）
        const dx = player.position.x - enemy.meshGroup.position.x;
        const dz = player.position.z - enemy.meshGroup.position.z;
        const targetAngle = Math.atan2(dx, dz);
        enemy.meshGroup.rotation.y = THREE.MathUtils.lerp(enemy.meshGroup.rotation.y, targetAngle, 5 * dt);
    }
}

// 敵の復活
function respawnEnemy() {
    enemy.isDead = false;

    // プレイヤーから12〜25ユニット離れた位置にランダム配置
    const angle = Math.random() * Math.PI * 2;
    const distance = 12 + Math.random() * 13;
    enemy.position.set(
        player.position.x + Math.sin(angle) * distance,
        0.9,
        player.position.z + Math.cos(angle) * distance
    );

    enemy.meshGroup.position.copy(enemy.position);
    enemy.meshGroup.rotation.set(0, 0, 0); // 回転リセット
}

// --- Main Animation Loop ---
function animate() {
    requestAnimationFrame(animate);

    const dt = clock.getDelta();

    if (isLocked) {
        // 1. プレイヤーの移動処理
        // プレイヤーの向きをカメラの水平角度(yaw)に同期
        player.mesh.rotation.y = yaw;

        // カメラの水平方向の前方ベクトルと右方向ベクトルを計算
        // yaw=0の時、カメラの正面は+Z方向
        const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw);
        const right = new THREE.Vector3(1, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), yaw);

        const moveDir = new THREE.Vector3();
        if (keys.w) moveDir.add(forward);
        if (keys.s) moveDir.sub(forward);
        if (keys.a) moveDir.add(right); // 左は right を足す
        if (keys.d) moveDir.sub(right); // 右は right を引く
        moveDir.normalize();

        player.velocity.x = moveDir.x * player.speed;
        player.velocity.z = moveDir.z * player.speed;

        // 重力とジャンプの適用
        if (!player.isGrounded) {
            player.velocity.y -= player.gravity * dt;
        } else {
            player.velocity.y = 0;
            if (keys.space) {
                player.velocity.y = player.jumpForce;
                player.isGrounded = false;
            }
        }

        // 位置更新と衝突判定の解決
        const oldPos = player.position.clone();

        // X軸移動と衝突解決
        player.position.x += player.velocity.x * dt;
        resolveCollisions('x', oldPos);

        // Z軸移動と衝突解決
        player.position.z += player.velocity.z * dt;
        resolveCollisions('z', oldPos);

        // Y軸移動と衝突解決
        player.isGrounded = false;
        player.position.y += player.velocity.y * dt;
        resolveCollisions('y', oldPos);

        // 地面衝突判定
        const halfHeight = player.height / 2;
        if (player.position.y < halfHeight) {
            player.position.y = halfHeight;
            player.velocity.y = 0;
            player.isGrounded = true;
        }

        // プレイヤーメッシュの位置を同期
        player.mesh.position.copy(player.position);

        // 銃の射撃反動リカバリー
        if (gunMesh && gunMesh.position.z > 0.2) {
            gunMesh.position.z = THREE.MathUtils.lerp(gunMesh.position.z, 0.2, 10 * dt);
        }

        // 2. カメラ位置の更新 (三人称視点 TPS)
        const targetCamX = player.position.x - Math.sin(yaw) * Math.cos(pitch) * cameraDistance;
        const targetCamZ = player.position.z - Math.cos(yaw) * Math.cos(pitch) * cameraDistance;
        const targetCamY = player.position.y + cameraHeightOffset - Math.sin(pitch) * cameraDistance;

        camera.position.set(targetCamX, targetCamY, targetCamZ);

        const lookTarget = new THREE.Vector3(
            player.position.x,
            player.position.y + cameraLookAtOffset,
            player.position.z
        );
        camera.lookAt(lookTarget);

        // 3. 建築プレビューの位置更新
        updatePreviewPosition();
    }

    // 弾丸の更新
    updateBullets(dt);

    // 敵の更新
    updateEnemy(dt);

    // レンダリング
    renderer.render(scene, camera);
}

// 起動
window.onload = init;
