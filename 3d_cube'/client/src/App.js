import { Canvas } from "@react-three/fiber";
import { useGLTF, Stage, PresentationControls } from "@react-three/drei";

function Model(props) {
  const { scene } = useGLTF("/cube.glb");
  return <primitive object={scene} {...props} />
}

function App() {
  return (
    <Canvas dpr={[1,2]} shadows camera={{fov: 45}}  style={{"position": "absolute"}}>
      <color attach="background" args={["#101010"]} />
      <PresentationControls speed={1.5} global zoom={.5} >
        <Stage environment={null}>
          <Model scale={2}/>
        </Stage>
      </PresentationControls >
    </Canvas>
  );
}

export default App;
