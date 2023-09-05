import Order from "./Components/orderComponent.tsx"

function App() {
  return (
    <div className="flex flex-col h-screen bg-slate-400">  
      <div className="grow-[1]">Advantech LTD Product Ordering System</div>
      <div className="grow-[10] flex flex-row">
        <div className="grow "></div>
        <Order></Order>
        <div className="grow "></div>
      </div>
      <div className=" grow-[1.5]">2</div>
    </div>
  )
}

export default App
