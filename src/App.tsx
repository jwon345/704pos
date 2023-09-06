import Order from "./Components/orderComponent.tsx";
import Header from './Components/header.tsx';

function App() {
  return (
    <div className="flex flex-col h-screen bg-slate-400">  
      <Header/>
      <div className="grow-[10] flex flex-row">
        <div className="grow "></div>
        <Order></Order>
        <div className="grow "></div>
      </div>
      <div className=" grow-[1.5]">:)</div>
    </div>
  )
}

export default App
