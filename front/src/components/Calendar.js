import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
 
export default function CalendarCfg({setEndDate,setStartDate}) {
    const [date, setDate] = useState(new Date());
    const [show, toggleShow] = useState(false);

    const handleDateChange = (date) => {
        setDate(date);
        if (date.length === 2) { // Assuming a range is selected
            setStartDate(date[0]);
            setEndDate(date[1]);
        }
    };

    return (
        <div>
            <button className="show-calendar-btn"  onClick={() => toggleShow(!show)}> <CalendarMonthOutlinedIcon /> Show Calendar</button>
            {show &&
            <div>
                <Calendar
                onChange={handleDateChange}
                value={date}
                selectRange={true}  
                dateFormat="dd/mm/yy"            
                  />
            {date.length > 0 ? (
            <p className='text-center'>
            <span className='bold'>Start:</span>{' '}
            {date[0].toDateString()}
             &nbsp;|&nbsp;
            <span className='bold'>End:</span> {date[1].toDateString()}
            </p>
            ) : (
            <p className='text-center'>
            <span className='bold'>Default selected date:</span>{' '}
            {date.toDateString()}
            </p>
            )}
            </div>
            }
            </div>
    );
}