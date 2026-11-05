import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export default function World() {
  const host = useRef<HTMLDivElement>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    const node = host.current;
    if (!node) return;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'low-power' }); }
    catch { setFailed(true); return; }
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.7));
    node.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(34, 1, .1, 100);
    camera.position.set(7.5, 6.2, 9.5); camera.lookAt(0, 0, 0);
    const world = new THREE.Group(); scene.add(world);
    const geometry = new THREE.BoxGeometry(.94, .94, .94);
    const dark = new THREE.MeshStandardMaterial({ color: '#2d3c49', metalness: .65, roughness: .3 });
    const blue = new THREE.MeshStandardMaterial({ color: '#326d83', metalness: .5, roughness: .24 });
    const glow = new THREE.MeshStandardMaterial({ color: '#8cf4e5', emissive: '#2eaca1', emissiveIntensity: .65, metalness: .3, roughness: .25 });
    const edges = new THREE.EdgesGeometry(geometry);
    const edgeMat = new THREE.LineBasicMaterial({ color: '#819eaa', transparent: true, opacity: .22 });
    const cubes: THREE.Mesh[] = [];
    for (let x = -2; x <= 2; x++) for (let z = -2; z <= 2; z++) {
      if ((x === -2 && z === 2) || (x === 2 && z === -2)) continue;
      const height = x === 0 && z === 0 ? 3 : (x + z + 6) % 3 === 0 ? 2 : 1;
      for (let y = 0; y < height; y++) {
        const lit = (x === 1 && z === 0) || (x === -1 && z === 1 && y === 1);
        const cube = new THREE.Mesh(geometry, lit ? glow : y > 0 ? blue : dark);
        cube.position.set(x * 1.04, y * 1.04 - 1, z * 1.04);
        cube.add(new THREE.LineSegments(edges, edgeMat)); world.add(cube); cubes.push(cube);
      }
    }
    const ringGeo = new THREE.TorusGeometry(4.1, .009, 4, 100);
    const ringMat = new THREE.MeshBasicMaterial({ color: '#477b85', transparent: true, opacity: .4 });
    const ring = new THREE.Mesh(ringGeo, ringMat); ring.rotation.x = Math.PI / 2; ring.position.y = -1.7; world.add(ring);
    scene.add(new THREE.HemisphereLight('#c7e6ff', '#131721', 2.6));
    const key = new THREE.DirectionalLight('#b9f8ef', 4); key.position.set(2, 6, 4); scene.add(key);
    const rim = new THREE.PointLight('#4860ff', 55, 18); rim.position.set(-4, 1, -3); scene.add(rim);
    const resize = () => { const { width, height } = node.getBoundingClientRect(); renderer.setSize(width, height); camera.aspect = width / Math.max(height,1); camera.updateProjectionMatrix(); };
    const ro = new ResizeObserver(resize); ro.observe(node); resize();
    let px = 0, py = 0, frame = 0, visible = true;
    const move = (e: PointerEvent) => { const r = node.getBoundingClientRect(); px = ((e.clientX-r.left)/r.width-.5)*.3; py = ((e.clientY-r.top)/r.height-.5)*.1; };
    node.addEventListener('pointermove', move);
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    const observer = new IntersectionObserver(([e]) => { visible=e.isIntersecting; }); observer.observe(node);
    const draw = (time: number) => { frame=requestAnimationFrame(draw); if (!visible || document.hidden) return; world.rotation.y += ((media.matches ? -.25 : -.25+px+Math.sin(time*.00013)*.08)-world.rotation.y)*.035; world.rotation.x += ((media.matches ? 0 : py)-world.rotation.x)*.035; if (!media.matches) cubes.forEach((c,i)=>{ if(i%9===0) c.position.y += Math.sin(time*.001+i)*.0007; }); renderer.render(scene,camera); };
    frame=requestAnimationFrame(draw);
    return () => { cancelAnimationFrame(frame); ro.disconnect(); observer.disconnect(); node.removeEventListener('pointermove',move); geometry.dispose(); edges.dispose(); dark.dispose(); blue.dispose(); glow.dispose(); edgeMat.dispose(); ringGeo.dispose(); ringMat.dispose(); renderer.dispose(); renderer.domElement.remove(); };
  }, []);
  return <div className="world" ref={host} role="img" aria-label="Abstract modular world of illuminated puzzle blocks">{failed && <div className="world-fallback"><span>◇</span><span>◇</span><span>◇</span></div>}<div className="world-caption"><span className="dot"/> INTERACTIVE SYSTEM / 001 <span>UNITY · XR · PLAY</span></div></div>;
}
