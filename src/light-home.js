import * as THREE from 'three';
import { InteractionManager } from 'three/addons/interaction/InteractionManager.js';
import { installHtmlInCanvasPolyfill } from 'three-html-render/polyfill';

const INITIAL_LIGHT = { enabled: true, angle: 34, brightness: 1450, color: '#ff9b45' };
const COLOR_PRESETS = ['#ff9b45', '#ffd89a', '#f06d3d', '#55c9ff', '#ad78ff'];
const CONCEPTS = {
  '服务破冰': '先解决一个明确的小麻烦，客户才愿意说出更多真实需求。',
  '发言入库': '把客户原话、家庭场景、预算与犹豫点沉淀为可复盘的需求证据。',
  '需求复盘': '每周识别重复出现的问题，不凭感觉扩张，只追踪真实高频需求。',
  '产品化': '把验证过的高频需求变成套餐、清单、上门 SOP、会员权益与产品。'
};

const shell = document.getElementById('experience');
const canvas = document.getElementById('lightCanvas');
const pageSurface = document.getElementById('pageSurface');
const errorElement = document.getElementById('sceneError');

function fail(message, error) {
  console.error(message, error || '');
  shell.classList.add('has-error');
  shell.setAttribute('aria-busy', 'false');
  errorElement.textContent = message;
}

function installThreeHtmlTextureCompatibility() {
  if (!window.__HTML_IN_CANVAS_POLYFILL__) return;
  for (const contextConstructor of [globalThis.WebGLRenderingContext, globalThis.WebGL2RenderingContext]) {
    if (!contextConstructor) continue;
    const prototype = contextConstructor.prototype;
    const uploadElement = prototype.texElementImage2D;
    if (!uploadElement || uploadElement.length !== 3) continue;
    Object.defineProperty(prototype, 'texElementImage2D', {
      configurable: true,
      writable: true,
      value(target, level, internalFormat, format, type, source) {
        uploadElement.call(this, target, level, internalFormat, format, type, source);
      }
    });
  }
}

async function startExperience() {
  canvas.setAttribute('layoutsubtree', '');
  installHtmlInCanvasPolyfill();
  installThreeHtmlTextureCompatibility();
  await new Promise((resolve) => requestAnimationFrame(resolve));

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
  } catch (error) {
    fail('当前浏览器无法创建 WebGL 场景，已保留静态首页。', error);
    return;
  }

  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1.08;
  renderer.setClearColor(0x030303, 1);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x030303);
  const camera = new THREE.PerspectiveCamera(37, 1, 0.1, 80);
  const pageGroup = new THREE.Group();
  pageGroup.position.set(0, -0.38, 0);
  scene.add(pageGroup);

  const pageTexture = new THREE.HTMLTexture(pageSurface);
  pageTexture.colorSpace = THREE.SRGBColorSpace;
  pageTexture.minFilter = THREE.LinearFilter;
  pageTexture.magFilter = THREE.LinearFilter;
  pageTexture.generateMipmaps = false;

  const pageGeometry = new THREE.PlaneGeometry(1, 1);
  const pageMaterial = new THREE.MeshStandardMaterial({
    map: pageTexture,
    color: 0xffffff,
    emissive: 0xffffff,
    emissiveMap: pageTexture,
    emissiveIntensity: 0.34,
    roughness: 0.96,
    metalness: 0,
    transparent: true,
    alphaTest: 0.005,
    side: THREE.FrontSide
  });
  const pageMesh = new THREE.Mesh(pageGeometry, pageMaterial);
  pageGroup.add(pageMesh);

  const backing = new THREE.Mesh(
    new THREE.PlaneGeometry(1.018, 1.028),
    new THREE.MeshStandardMaterial({ color: 0x080503, roughness: 0.92, metalness: 0.02 })
  );
  backing.position.z = -0.035;
  pageGroup.add(backing);

  scene.add(new THREE.HemisphereLight(0x8a684f, 0x100a07, 0.5));
  const fillLight = new THREE.DirectionalLight(0xffd2aa, 0.18);
  fillLight.position.set(-4.8, 5.6, 7.4);
  scene.add(fillLight);

  const lampRoot = new THREE.Group();
  scene.add(lampRoot);
  const anchor = new THREE.Vector3(0, 4.72, 1.18);
  const ropeLength = 1.22;
  const pageTopToAnchor = 1.18;

  const ceilingCap = new THREE.Mesh(
    new THREE.CylinderGeometry(0.24, 0.3, 0.11, 24),
    new THREE.MeshStandardMaterial({ color: 0x17100d, roughness: 0.62, metalness: 0.72 })
  );
  ceilingCap.position.copy(anchor).add(new THREE.Vector3(0, 0.08, 0));
  scene.add(ceilingCap);

  const cable = new THREE.Mesh(
    new THREE.CylinderGeometry(0.014, 0.014, 1, 10),
    new THREE.MeshStandardMaterial({ color: 0x241b17, roughness: 0.5, metalness: 0.55 })
  );
  scene.add(cable);

  const shadeGroup = new THREE.Group();
  lampRoot.add(shadeGroup);
  const shadeProfile = [
    new THREE.Vector2(0.08, 0.08), new THREE.Vector2(0.18, 0.02),
    new THREE.Vector2(0.43, -0.1), new THREE.Vector2(0.82, -0.25),
    new THREE.Vector2(1.08, -0.36), new THREE.Vector2(1.1, -0.41)
  ];
  const shadeMaterial = new THREE.MeshStandardMaterial({ color: 0x17110e, roughness: 0.34, metalness: 0.72, side: THREE.DoubleSide });
  const shade = new THREE.Mesh(new THREE.LatheGeometry(shadeProfile, 48), shadeMaterial);
  shadeGroup.add(shade);
  const rim = new THREE.Mesh(
    new THREE.TorusGeometry(1.095, 0.027, 8, 48),
    new THREE.MeshStandardMaterial({ color: 0x2a1c15, roughness: 0.28, metalness: 0.82 })
  );
  rim.rotation.x = Math.PI / 2;
  rim.position.y = -0.397;
  shadeGroup.add(rim);

  const undersideMaterial = new THREE.MeshStandardMaterial({
    color: new THREE.Color(INITIAL_LIGHT.color).multiplyScalar(0.18),
    emissive: INITIAL_LIGHT.color,
    emissiveIntensity: 0.42,
    roughness: 0.92,
    side: THREE.DoubleSide
  });
  const underside = new THREE.Mesh(new THREE.CircleGeometry(1.055, 48), undersideMaterial);
  underside.rotation.x = Math.PI / 2;
  underside.position.y = -0.385;
  shadeGroup.add(underside);

  const bulbMaterial = new THREE.MeshStandardMaterial({ color: 0xfff1dd, emissive: INITIAL_LIGHT.color, emissiveIntensity: 3.2, roughness: 0.2 });
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 12), bulbMaterial);
  bulb.scale.y = 1.2;
  bulb.position.y = -0.33;
  shadeGroup.add(bulb);

  const glowTexture = createGlowTexture();
  const glowMaterial = new THREE.SpriteMaterial({ map: glowTexture, color: INITIAL_LIGHT.color, transparent: true, opacity: 0.86, depthWrite: false, blending: THREE.AdditiveBlending });
  const glow = new THREE.Sprite(glowMaterial);
  glow.position.y = -0.36;
  glow.scale.set(0.96, 0.96, 0.96);
  shadeGroup.add(glow);

  const spot = new THREE.SpotLight(INITIAL_LIGHT.color, 1, 18, THREE.MathUtils.degToRad(INITIAL_LIGHT.angle), 0.88, 2);
  spot.power = INITIAL_LIGHT.brightness;
  spot.position.set(0, -0.35, 0);
  spot.target.position.set(0, -7, 0);
  shadeGroup.add(spot, spot.target);
  const bulbLight = new THREE.PointLight(INITIAL_LIGHT.color, 1, 3.2, 2);
  bulbLight.power = 36;
  bulbLight.position.set(0, -0.35, 0);
  shadeGroup.add(bulbLight);

  const interactions = new InteractionManager();
  interactions.connect(renderer, camera);
  interactions.add(pageMesh);

  const fixedStep = 1 / 120;
  const gravity = new THREE.Vector3(0, -9.81, 0);
  const position = new THREE.Vector3(0.16, anchor.y - ropeLength, anchor.z + 0.08);
  const previous = position.clone().add(new THREE.Vector3(0.018, 0, -0.012));
  const aimTarget = new THREE.Vector3(0, 0.3, 0.08);
  const pointerVelocity = new THREE.Vector3();
  const lastPointerTarget = aimTarget.clone();
  const pointer = new THREE.Vector2();
  const raycaster = new THREE.Raycaster();
  const interactionPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -0.08);
  const down = new THREE.Vector3(0, -1, 0);
  const up = new THREE.Vector3(0, 1, 0);
  const baseLightDirection = down.clone();
  const temp = new THREE.Vector3();
  const tempB = new THREE.Vector3();
  const tempC = new THREE.Vector3();
  const velocity = new THREE.Vector3();
  const ropeDirection = new THREE.Vector3();
  const lightDirection = new THREE.Vector3();
  const currentLightDirection = baseLightDirection.clone();
  const midpoint = new THREE.Vector3();
  const swingQuaternion = new THREE.Quaternion();
  const lampQuaternion = new THREE.Quaternion();
  const cableQuaternion = new THREE.Quaternion();
  const lampNdc = new THREE.Vector3();
  let pulling = false;
  let pullPointerId = -1;
  let pullStrength = 0;
  let lastPointerTime = 0;
  let beamPointerId = -1;
  let beamStartX = 0;
  let beamStartAngle = INITIAL_LIGHT.angle;
  let beamDragged = false;
  let accumulator = 0;
  let lastFrameTime = performance.now();
  let disposed = false;
  let readyFrames = 0;

  const lighting = { ...INITIAL_LIGHT };
  const powerToggle = pageSurface.querySelector('#powerToggle');
  const beamRange = pageSurface.querySelector('#beamRange');
  const brightnessRange = pageSurface.querySelector('#brightnessRange');
  const beamOutput = pageSurface.querySelector('#beamOutput');
  const brightnessOutput = pageSurface.querySelector('#brightnessOutput');
  const colorOutput = pageSurface.querySelector('#colorOutput');
  const resetButton = pageSurface.querySelector('#resetLight');
  const colorButtons = [...pageSurface.querySelectorAll('[data-color]')];

  function createGlowTexture() {
    const textureCanvas = document.createElement('canvas');
    textureCanvas.width = 64;
    textureCanvas.height = 64;
    const context = textureCanvas.getContext('2d');
    const gradient = context.createRadialGradient(32, 32, 0, 32, 32, 32);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.16, 'rgba(255,222,172,.8)');
    gradient.addColorStop(0.46, 'rgba(255,154,69,.22)');
    gradient.addColorStop(1, 'rgba(255,140,70,0)');
    context.fillStyle = gradient;
    context.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(textureCanvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    return texture;
  }

  function updateLighting() {
    const color = new THREE.Color(lighting.color);
    const effectiveBrightness = lighting.enabled ? lighting.brightness : 0;
    spot.color.copy(color);
    spot.power = effectiveBrightness;
    spot.angle = THREE.MathUtils.degToRad(lighting.angle);
    bulbLight.color.copy(color);
    bulbLight.power = lighting.enabled ? 36 : 0;
    bulbMaterial.emissive.copy(color);
    bulbMaterial.emissiveIntensity = lighting.enabled ? 3.2 : 0.03;
    glowMaterial.color.copy(color);
    glowMaterial.opacity = lighting.enabled ? 0.86 : 0.08;
    undersideMaterial.emissive.copy(color);
    undersideMaterial.emissiveIntensity = lighting.enabled ? 0.22 + lighting.brightness / 7250 : 0.03;
    pageSurface.style.setProperty('--lamp-color', lighting.color);
    beamRange.value = String(lighting.angle);
    brightnessRange.value = String(lighting.brightness);
    beamOutput.textContent = `${lighting.angle}°`;
    brightnessOutput.textContent = `${lighting.brightness} lm`;
    colorOutput.textContent = lighting.color.toUpperCase();
    powerToggle.classList.toggle('is-on', lighting.enabled);
    powerToggle.setAttribute('aria-pressed', String(lighting.enabled));
    powerToggle.querySelector('span').textContent = lighting.enabled ? 'ON' : 'OFF';
    colorButtons.forEach((button) => button.classList.toggle('is-active', button.dataset.color.toLowerCase() === lighting.color.toLowerCase()));
    canvas.requestPaint?.();
  }

  function resetMotion() {
    position.set(0.16, anchor.y - ropeLength, anchor.z + 0.08);
    previous.copy(position).add(new THREE.Vector3(0.018, 0, -0.012));
    currentLightDirection.copy(baseLightDirection);
  }

  function resetAll() {
    Object.assign(lighting, INITIAL_LIGHT);
    updateLighting();
    resetMotion();
  }

  powerToggle.addEventListener('click', () => { lighting.enabled = !lighting.enabled; updateLighting(); });
  beamRange.addEventListener('input', () => { lighting.angle = Number(beamRange.value); updateLighting(); });
  brightnessRange.addEventListener('input', () => { lighting.brightness = Number(brightnessRange.value); updateLighting(); });
  colorButtons.forEach((button) => button.addEventListener('click', () => { lighting.color = button.dataset.color; updateLighting(); }));
  resetButton.addEventListener('click', resetAll);

  const conceptDescription = pageSurface.querySelector('#conceptDescription');
  pageSurface.querySelectorAll('[data-concept]').forEach((button) => button.addEventListener('click', () => {
    pageSurface.querySelectorAll('[data-concept]').forEach((entry) => entry.classList.toggle('is-active', entry === button));
    conceptDescription.innerHTML = `<span>${button.dataset.concept}</span>${CONCEPTS[button.dataset.concept]}`;
    canvas.requestPaint?.();
  }));

  function resize() {
    const width = Math.max(1, canvas.clientWidth);
    const height = Math.max(1, canvas.clientHeight);
    const dpr = Math.min(window.devicePixelRatio || 1, width < 760 ? 1.25 : 1.5);
    renderer.setPixelRatio(dpr);
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    const sourceWidth = pageSurface.offsetWidth || 1440;
    const sourceHeight = pageSurface.offsetHeight || 810;
    const portrait = height > width * 1.16;
    const pageWidth = portrait ? 7.2 : 12.8;
    const pageHeight = pageWidth * (sourceHeight / sourceWidth);
    pageMesh.scale.set(pageWidth, pageHeight, 1);
    backing.scale.set(pageWidth, pageHeight, 1);
    pageGroup.position.y = portrait ? -0.62 : -0.38;
    anchor.set(0, pageGroup.position.y + pageHeight / 2 + pageTopToAnchor, portrait ? 1.1 : 1.18);
    ceilingCap.position.copy(anchor).add(new THREE.Vector3(0, 0.08, 0));
    if (!pulling) {
      const constrained = temp.copy(position).sub(anchor);
      if (constrained.lengthSq() < 0.001) constrained.copy(down);
      constrained.normalize().multiplyScalar(ropeLength);
      position.copy(anchor).add(constrained);
      previous.copy(position);
    }
    const fitHeight = pageHeight + 3.1;
    const fitWidth = pageWidth + 1.25;
    const halfFov = THREE.MathUtils.degToRad(camera.fov * 0.5);
    const distanceForHeight = fitHeight / (2 * Math.tan(halfFov));
    const distanceForWidth = fitWidth / (2 * Math.tan(halfFov) * camera.aspect);
    const cameraDistance = Math.max(distanceForHeight, distanceForWidth);
    camera.position.set(0, pageGroup.position.y - (portrait ? 0.78 : 0.62), cameraDistance);
    camera.lookAt(0, pageGroup.position.y + (portrait ? -0.04 : 0.06), 0);
    camera.updateMatrixWorld();
    interactions.update();
    canvas.requestPaint?.();
  }

  function pointerNdc(event) {
    const rect = canvas.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
  }

  function updatePointerTarget(event) {
    pointerNdc(event);
    if (!raycaster.ray.intersectPlane(interactionPlane, aimTarget)) return false;
    lampNdc.copy(position).project(camera);
    const distanceX = (pointer.x - lampNdc.x) * camera.aspect;
    const distanceY = pointer.y - lampNdc.y;
    pullStrength = THREE.MathUtils.smoothstep(Math.sqrt(distanceX * distanceX + distanceY * distanceY), 0.08, 1.15);
    return true;
  }

  function onPointerDown(event) {
    if (event.button === 2) {
      beamPointerId = event.pointerId;
      beamStartX = event.clientX;
      beamStartAngle = lighting.angle;
      beamDragged = false;
      return;
    }
    if (event.button !== 0 || beamPointerId !== -1) return;
    if (event.target instanceof Element && event.target.closest('[data-interactive],a,button,input,label')) return;
    if (!updatePointerTarget(event)) return;
    pulling = true;
    pullPointerId = event.pointerId;
    event.preventDefault();
    lastPointerTime = performance.now();
    lastPointerTarget.copy(aimTarget);
    pointerVelocity.set(0, 0, 0);
    shell.classList.add('is-pulling');
  }

  function onPointerMove(event) {
    if (event.pointerId === beamPointerId) {
      const movementX = event.clientX - beamStartX;
      if (!beamDragged && Math.abs(movementX) >= 4) beamDragged = true;
      if (beamDragged) {
        lighting.angle = THREE.MathUtils.clamp(Math.round(beamStartAngle + movementX * 0.14), 16, 58);
        updateLighting();
      }
      return;
    }
    if (!pulling || event.pointerId !== pullPointerId || !updatePointerTarget(event)) return;
    const now = performance.now();
    const elapsed = Math.max(0.008, Math.min(0.05, (now - lastPointerTime) / 1000));
    temp.copy(aimTarget).sub(lastPointerTarget).multiplyScalar(1 / elapsed);
    pointerVelocity.lerp(temp, 0.34);
    lastPointerTarget.copy(aimTarget);
    lastPointerTime = now;
  }

  function onPointerUp(event) {
    if (event.pointerId === beamPointerId) {
      const shouldCycleColor = !beamDragged && event.type !== 'pointercancel';
      beamPointerId = -1;
      beamDragged = false;
      if (shouldCycleColor) {
        const currentIndex = COLOR_PRESETS.indexOf(lighting.color.toLowerCase());
        lighting.color = COLOR_PRESETS[(currentIndex + 1) % COLOR_PRESETS.length];
        updateLighting();
      }
      return;
    }
    if (!pulling || event.pointerId !== pullPointerId) return;
    pulling = false;
    pullPointerId = -1;
    shell.classList.remove('is-pulling');
    previous.copy(position).addScaledVector(pointerVelocity, -fixedStep * 0.36);
  }

  function stepPhysics() {
    velocity.copy(position).sub(previous).multiplyScalar(pulling ? 0.985 : 0.9948);
    previous.copy(position);
    position.add(velocity).addScaledVector(gravity, fixedStep * fixedStep);
    if (pulling) {
      tempB.copy(aimTarget).sub(anchor).normalize();
      tempB.lerp(down, 1 - pullStrength * 0.82).normalize();
      tempC.copy(tempB).multiplyScalar(ropeLength).add(anchor).sub(position);
      temp.copy(position).sub(anchor).normalize();
      tempC.addScaledVector(temp, -tempC.dot(temp));
      position.addScaledVector(tempC, 52 * fixedStep * fixedStep);
    }
    temp.copy(position).sub(anchor);
    if (temp.lengthSq() < 1e-8) temp.copy(down);
    temp.normalize().multiplyScalar(ropeLength);
    position.copy(anchor).add(temp);
  }

  function updateRig() {
    ropeDirection.copy(position).sub(anchor).normalize();
    midpoint.copy(anchor).add(position).multiplyScalar(0.5);
    cable.position.copy(midpoint);
    cable.scale.set(1, ropeLength, 1);
    cableQuaternion.setFromUnitVectors(up, ropeDirection);
    cable.quaternion.copy(cableQuaternion);
    if (pulling) {
      lightDirection.copy(aimTarget).sub(position).normalize();
      currentLightDirection.lerp(lightDirection, 0.32).normalize();
    } else {
      swingQuaternion.setFromUnitVectors(down, ropeDirection);
      lightDirection.copy(baseLightDirection).applyQuaternion(swingQuaternion).normalize();
      currentLightDirection.lerp(lightDirection, 0.14).normalize();
    }
    lampQuaternion.setFromUnitVectors(down, currentLightDirection);
    lampRoot.position.copy(position);
    lampRoot.quaternion.copy(lampQuaternion);
  }

  function animate(time) {
    if (disposed) return;
    const delta = Math.min((time - lastFrameTime) / 1000, 0.05);
    lastFrameTime = time;
    accumulator = Math.min(accumulator + delta, fixedStep * 5);
    while (accumulator >= fixedStep) {
      stepPhysics();
      accumulator -= fixedStep;
    }
    updateRig();
    interactions.update();
    renderer.render(scene, camera);
    if (++readyFrames === 3) {
      shell.classList.add('is-ready');
      shell.setAttribute('aria-busy', 'false');
    }
    requestAnimationFrame(animate);
  }

  canvas.addEventListener('pointerdown', onPointerDown);
  canvas.addEventListener('dblclick', resetMotion);
  canvas.addEventListener('contextmenu', (event) => event.preventDefault());
  window.addEventListener('pointermove', onPointerMove);
  window.addEventListener('pointerup', onPointerUp);
  window.addEventListener('pointercancel', onPointerUp);
  window.addEventListener('resize', resize);
  canvas.addEventListener('paint', () => { pageTexture.needsUpdate = true; });
  window.addEventListener('pagehide', () => { disposed = true; interactions.disconnect(); renderer.dispose(); }, { once: true });

  updateLighting();
  resize();
  canvas.requestPaint?.();
  requestAnimationFrame(animate);
}

startExperience().catch((error) => fail('HTML-in-Canvas 初始化失败，已保留静态首页。', error));
