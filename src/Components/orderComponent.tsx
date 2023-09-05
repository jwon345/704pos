import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';

import { useState, SetStateAction, Dispatch } from 'react';


function Order() {

  const [v1, setv1] = useState(25);
  const [v2, setv2] = useState(25);
  const [v3, setv3] = useState(25);
  const [v4, setv4] = useState(25);

    return (
        <div className="grow-[10] bg-gray-300 rounded-3xl flex flex-col p-10 shadow-lg">
          <Button variant='contained'>hello</Button>
          <div className='m-4'>
          <CustomSlider setVal={setv1} other1={v2} other2={v3} other3={v4} />
          </div>
          <div className='m-4'>
            <CustomSlider setVal={setv2} other1={v1} other2={v3} other3={v4} />
          </div>
          <div className='m-4'>
            <SliderHeader name="Liquid3" value={v3}/>
            <CustomSlider setVal={setv3} other1={v1} other2={v2} other3={v4} />
          </div>
          <div className='m-4'>
            <h1 className='border'>Liquid4 {v4}%</h1>
            <CustomSlider setVal={setv4} other1={v1} other2={v2} other3={v3} />
          </div>
        </div>
    )
}

type CustomSliderProps = {
  setVal: Dispatch<SetStateAction<number>>;
  other1: number;
  other2: number;
  other3: number;
};
const marks = [
  {
    value: 0,
    label: '0%',
  },
  {
    value: 20,
    label: '20°%',
  },
  {
    value: 40,
    label: '40%',
  },
  {
    value: 60,
    label: '60%',
  },
  {
    value: 80,
    label: '80%',
  },
  {
    value: 100,
    label: '100°C',
  },
];

interface SliderHeaderProps{
  name:string
  value:number
}

const SliderHeader: React.FC<SliderHeaderProps> = ({ name, value }) => {
  return <h1>{name} {value}%</h1>;
}

const CustomSlider: React.FC<CustomSliderProps> = ({ setVal, other1, other2, other3 }) => {
  return (
    <Slider 
      // aria-label="Always visible"  
      valueLabelDisplay="auto" 
      size="medium" 
      defaultValue={25} 
      step={1} 
      marks={marks} 
      min={0} 
      max={100 - other1 - other2 - other3}
      onChange={(_, newValue) => setVal(newValue as number)}
    />
  );
}

export default Order;

