// This is a custom React Hook from 
// https://overreacted.io/making-setinterval-declarative-with-react-hooks/
//
// Usage example:
//
//  import React, { useState, useEffect, useRef } from 'react';
//  
//  function Counter() {
//    let [count, setCount] = useState(0);
//  
//    useInterval(() => {
//      // Your custom logic here
//      setCount(count + 1);
//    }, 1000);
//  
//    return <h1>{count}</h1>;
//  }



import React, { useState, useEffect, useRef } from 'react';

export default function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}
