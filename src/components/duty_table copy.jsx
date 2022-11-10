import Table from 'react-bootstrap/Table';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Form from 'react-bootstrap/Form';
import React, {Component} from 'react';


// var stat = require('./data/status.json')
var dt = require('./data/data.json') 

class DutyTable extends Component {

  state = { status: [], 
            id: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34], 
            duty: dt } 


  fetchStatus = async () => {
      const response = await fetch("https://wwl-server.herokuapp.com/status")
      const status_js = await response.json()
      console.log(status_js)
      this.setState({status: status_js})
      
    }
  
  componentDidMount () {
    this.fetchStatus()
  }

  handleClick = event => {
    let x = event.currentTarget.id
    this.handleCheck(x)
  };



  handleCheck = (x) => {
    console.log(x)
    let new_stat = this.state.status
    if (this.state.status[x] === 'checked')
      {new_stat[x] = ''
      this.setState({status: new_stat}) 
      console.log(this.state.status)
      fetch("https://wwl-server.herokuapp.com/saveStatus", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({'_id': x, 'status': ''})})
    }
    else {
    new_stat[x] = 'checked'
    this.setState({status: new_stat})
    console.log(this.state.status)
    fetch("https://wwl-server.herokuapp.com/saveStatus", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({'_id': x, 'status': 'checked'})}).then(console.log(this.state.status))
    }
  }

  renderSelected = (i) => {
    return <> <td><p className="text-decoration-line-through"> {this.state.duty.time[i]} </p></td>
              <td><p className="text-decoration-line-through"> {this.state.duty.activity[i]}</p></td>
              <td><p className="text-decoration-line-through"> {this.state.duty.estimated_time[i]} </p></td>
              <td><p className="text-decoration-line-through"> {this.state.duty.support[i]} </p></td>
           </>
    }

  renderRow = (i) =>  {
    return (<>  <td>{this.state.duty.time[i]}</td>
                <td>{this.state.duty.activity[i]}</td>
                <td>{this.state.duty.estimated_time[i]}</td>
                <td>{this.state.duty.support[i]}</td>
            </>)}

  renderTable = (i) => {
    if (this.state.status[i] === 'checked') 
      return     <>
      <th id={i} onChange={this.handleClick} scope="row"><Form.Check style={{width:30, height:30}} type="checkbox" class="custom-control-input" id="customCheck1" defaultChecked/></th>
      {this.renderSelected(i)}
  </>
    return   <>
    <th id={i} onChange={this.handleClick} scope="row"> <Form.Check style={{width:30, height:30}} type="checkbox" class="custom-control-input" id="customCheck1" /></th>
    {this.renderRow(i)}
    </>
  }

  render() { 
    
    return (
      <Container>
    <Row>
    <h3 className="text-center">Duty Manager Check List</h3>
    <h4 className="text-center">Nov 03, 2022</h4>
    </Row>
    <Row >
    <Table >
      <thead>
        <tr>
          <th scope="col"> </th>
          <th scope="col">Time</th>
          <th scope="col">Activity</th>
          <th scope="col">Estimated Time</th>
          <th scope="col">Support</th>
        </tr>
      </thead>

      <tbody>
        {this.state.id.map(i => <tr id={i} > {this.renderTable(i)}</tr>)}
      </tbody>
    </Table>
    </Row>
    </Container>);
  }
}
 
export default DutyTable;