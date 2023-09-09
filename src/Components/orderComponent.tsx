import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';
import Textfield from '@mui/material/TextField';
import SendIcon from '@mui/icons-material/Send';
import  Snackbar  from '@mui/material/Snackbar';
import Alert  from '@mui/material/Alert';


import { useState, useEffect, SetStateAction, Dispatch } from 'react';
import axios from 'axios';


function Order() {

  const [v1, setv1] = useState(25);
  const [v2, setv2] = useState(25);
  const [v3, setv3] = useState(25);
  const [v4, setv4] = useState(25);

  const [statusOk, setStatusOk] = useState(false);
  const [Status, setStatus] = useState("Ready");

  const [bottleNumber, setBottleNumber] = useState(1);

  const [open, setOpen] = useState(false);

  const [responseData, setResponseData] = useState(":)");
  
  const handleClick = () => {
    setOpen(true);
  };

  useEffect(() => {

      //Implementing the setInterval method
      const interval = setInterval(() => {
        axios.get("http://127.0.0.1:5000/Status")
        .then((response) => {
          setStatus(String(response.data));
          console.log(response);
        })
      }, 1000);

      //Clearing the interval
      return () => clearInterval(interval);
  }, [Status]);

  const handleClose = (event: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  }


    return (
        <div className="grow-[10] bg-gray-300 rounded-3xl flex flex-col p-10 shadow-lg">
          <div className='m-4'>
           <SliderHeader name="Liquid1" value={v1}/>
          <CustomSlider setVal={setv1} other1={v2} other2={v3} other3={v4} />
          </div>
          <div className='m-4'>
            <SliderHeader name="Liquid2" value={v2}/>
            <CustomSlider setVal={setv2} other1={v1} other2={v3} other3={v4} />
          </div>
          <div className='m-4'>
            <SliderHeader name="Liquid3" value={v3}/>
            <CustomSlider setVal={setv3} other1={v1} other2={v2} other3={v4} />
          </div>
          <div className='m-4'>
            <SliderHeader name="Liquid4" value={v4}/>
            <CustomSlider setVal={setv4} other1={v1} other2={v2} other3={v3} />
          </div>
          <div className='self-center mt-10' >
            <h1 className={Status.includes('Ready')?'text-green-500 text-2xl' :'text-red-500 text-2xl'}><b>{Status}</b></h1>
            {/* <h1 >{Status.includes('Ready')?'text-orange-500':'text-red-500'}</h1> */}
          </div>

          <div className='grow flex flex-col justify-end'>
            <div className='flex items-center'>
              <div className='grow '></div>
              <div className='w-80'>
                <Textfield 
                inputProps={{type:'number'}}
                fullWidth
                label="Order Number"
                defaultValue={1}
                onChange={(e) => {setBottleNumber(Number(e.target.value))}}
                variant='outlined'></Textfield>
              </div>
              <div className='grow '></div>
            </div>


            <div className='flex items-center m-2'>
              <div className='grow '></div>
              <div className='w-80'>
                <Button
                fullWidth
                variant='contained'
                endIcon={<SendIcon/>}
                onClick={() => axios.post("http://127.0.0.1:5000/newBot", {'number':{bottleNumber}.bottleNumber,'val':{v1}.v1})
                .then(function (response) {
                  console.log(response);
                  setResponseData(response.data);
                  {response.data == "BUSY" ? setStatusOk(false) :setStatusOk(true)}
                  
                  handleClick();
                })
                .catch(()=>{
                  setResponseData("not connected");
                  setStatusOk(false);
                  handleClick();
                })
              }
                >Place Order</Button>
              </div>
              <div className='grow '></div>
            </div>
           </div>
            <Snackbar
              open={open}
              autoHideDuration={2500}
              onClose={handleClose}
              message={responseData}
            >
              <Alert onClose={handleClose} severity={statusOk ? "success" : "error"} sx={{ width: '100%' }}>
               {responseData}
              </Alert>

            </Snackbar>
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
    label: '100%',
  },
];

interface SliderHeaderProps{
  name:string
  value:number
}

const SliderHeader: React.FC<SliderHeaderProps> = ({ name, value }) => {
  return <h1 className='text-xl'><b>{name} {value}%</b></h1>;
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

