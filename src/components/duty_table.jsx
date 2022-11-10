import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import React from 'react';
import db from './firebase';
import { useState, useEffect } from 'react';
import {collection, query, orderBy, onSnapshot, addDoc} from "firebase/firestore";


// var db_d =  db_data.get().then(function(snapshot) {var duties = []; snapshot.forEach(function(childSnapshot) {
//       var id = childSnapshot.id;
//       var data = childSnapshot.val();
//       duties.push({ id: id, title: data.title, description: data.description}); })})


export default function DutyTable() {
  
  const [duty, setDuty] = useState([]);
  const [status, setStat] = useState([])
  const [id, setId] = useState([])
  

 useEffect(() => { 
    // var status_db = db
    var stat = require('./data/status.json')
    var ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
    var dt = require('./data/data.json') 
    const q = query(collection(db, 'duty'), orderBy('created', 'desc'))
    console.log(q)
    onSnapshot(q, (querySnapshot) => {
      setDuty(querySnapshot.docs.map(doc => ({
        id: doc.id,
        data: doc.data()
      })))
    })

  

   setId(ids)
   setStat(stat.status)
  //  setDuty(dt) 
  }, []);

 

    const handleClick = event => {
      let x = event.currentTarget.id 
      handleCheck(x)
    };

    // const handleSubmit = async (e) => {
    //   e.preventDefault()
    //   try {
    //     await addDoc(collection(db, 'tasks'), {
    //       title: title,
    //       description: description,
    //       completed: false,
    //       created: Timestamp.now()
    //     })
    //     onClose()
    //   } catch (err) {
    //     alert(err)
    //   }
    // }
    const handleCheck = (x) => {
    let new_stat = status
    if (status[x] === 'checked')
      {new_stat[x] = ''
      setStat(new_stat)
      console.log(status)
      }
    else 
      {new_stat[x] = 'checked'
      setStat(new_stat)
      console.log(status)}
    }


  const renderSelected = (i) => {
    return <> <td><p className="text-decoration-line-through"> {duty.time[i]} </p></td>
              <td><p className="text-decoration-line-through"> {duty.activity[i]}</p></td>
              <td><p className="text-decoration-line-through"> {duty.estimated_time[i]} </p></td>
              <td><p className="text-decoration-line-through"> {duty.support[i]} </p></td>
           </>
    }


  const renderRow = (i) =>  {
    return (<>  <td>{duty.time[i]}</td>
                <td>{duty.activity[i]}</td>
                <td>{duty.estimated_time[i]}</td>
                <td>{duty.support[i]}</td>
            </>)
    }

  const renderTable = (i) => {
    if (status[i] === 'checked') 
      {return <>
      <th id={i} onChange={handleClick} scope="row"><Form.Check type="checkbox" class="custom-control-input" id="customCheck1" defaultChecked/></th>
      {renderSelected(i)}</>}
    else
      {return <>
      <th id={i} onChange={handleClick} scope="row"> <Form.Check type="checkbox" class="custom-control-input" id="customCheck1" /></th>
      {renderRow(i)}</>}
    }

    
  return (<Container className='me-3zzz'>
                <Row>
                  <h3>Duty Manager Check List</h3>
                  <h4>Nov 03, 2022</h4>
                </Row>

                <Row > 
                  <Table >
                    <thead> 
                      <tr>
                        <th scope="col"> </th> <th scope="col">Time</th> <th scope="col">Activity</th> <th scope="col">Estimated Time</th> <th scope="col">Support</th>
                      </tr> 
                    </thead>
                    <tbody>
                      {id.map(i => <tr id={i} > {renderTable(i)}</tr>)}
                    </tbody>
                  </Table> 
                </Row>
            </Container>)
}

