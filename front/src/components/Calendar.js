import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
 
export default function CalendarCfg(props) {
    const [date, onChange] = useState(new Date());
    const [show, toggleShow] = useState(false);

    return (
        <div>
            <button  onClick={() => toggleShow(!show)}>Show Calendar</button>
            {show &&
            <div>
                <Calendar
                onChange={onChange}
                value={date}
                selectRange={true}              
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