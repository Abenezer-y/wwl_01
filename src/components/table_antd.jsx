import { Layout, Divider, Checkbox , List, Typography, Button, Row, } from 'antd';
import React, {useState, useEffect} from 'react';
import './main.css';

const { Title, Text } = Typography;
const { Header, Content } = Layout;


var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
today = mm + '/' + dd + '/' + yyyy;

const Duty = () => {

    const [tdy, setTdy] = useState([])
    const [button_stat, setButn] = useState(true)
    const [list1, setList1] = useState([])
    const [list2, setList2] = useState([])
    const [list3, setList3] = useState([])
    const [list4, setList4] = useState([])
    const [list5, setList5] = useState([])
    const [list6, setList6] = useState([])
    const [list7, setList7] = useState([])
    const [list8, setList8] = useState([])
    const [list9, setList9] = useState([])
    const [list10, setList10] = useState([])

    const submit = () => {
        fetch("http://wwl-server.herokuapp.com/submit")
    }

    const fetchStatus = async () => {
        const response = await fetch("http://wwl-server.herokuapp.com/allData")
        const status_js = await response.json()

        setList1(status_js[0]) 
        setList2(status_js[1])
        setList3(status_js[2]) 
        setList4(status_js[3]) 
        setList5(status_js[4]) 
        setList6(status_js[5]) 
        setList7(status_js[6]) 
        setList8(status_js[7]) 
        setList9(status_js[8]) 
        setList10(status_js[9]) 
      }

    useEffect(() => {
        fetchStatus()
        setTdy(today)
        console.log('Data loaded')
    }, [])

//     const check_button = () => {
//         list1.map(item => {if (!item.status) return true})
//         list2.map(item => {if (!item.status) return true })
//         list3.map(item => {if (!item.status) return true })
//         list4.map(item => {if (!item.status) return true })
//         list5.map(item => {if (!item.status) return true })
//         list6.map(item => {if (!item.status) return true })
//         list7.map(item => {if (!item.status) return true })
//         list8.map(item => {if (!item.status) return true })
//         list9.map(item => {if (!item.status) return true })
//         list10.map(item => {if (!item.status) return true })
//         return false
//     }

    const handleCheck = (x, status) => {

        fetch("https://wwl-server.herokuapp.com/editStatus", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({'_id': x, 'status': status})})

        fetchStatus()
        }
      
    const croosOut = (status, text) => {
            if (status) 
                return <Text style={{textAlign: 'right',}} delete>{text}</Text>
            else
                return <Text style={{textAlign: 'right'}}>{text}</Text>
    
              };

    const onChange = (e) => {
        handleCheck(e.target.id, e.target.checked)
          };

    return (<>
    <Layout>
      <Header  style={{height:150, textAlign: 'center', padding:6}}>
      <Typography>
        <Title style={{color: "white", fontSize:28}}>
            Duty Manager Check List
        </Title>
        <Text style={{color: "white"}}>{tdy}</Text>
     </Typography>
      </Header>

      <Content>
        <Divider>Time - 15:30</Divider>
        <List size="small">
                {list1.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 1530-1630</Divider>
        <List size="small">
                {list2.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 16:30</Divider>
        <List size="small">
                {list3.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 17:00</Divider>
        <List size="small">
                {list4.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 17:30</Divider>
        <List size="small">
                {list5.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>2350/0050 (After close of final session)</Divider>
        <List size="small">
                {list6.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 0015/0115</Divider>
        <List size="small">
                {list7.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>After last guest leave skate exchange</Divider>
        <List size="small">
                {list8.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 15:30</Divider>
        <List size="small">
                {list9.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Divider>Time - 0130/0230</Divider>
        <List size="small">
                {list10.map(item => (<List.Item><Checkbox id={item.id} onChange={onChange} defaultChecked={item.status}>{croosOut(item.status, item.activity)}</Checkbox></List.Item>))}
        </List>
        <Row type="flex" justify="center">
                <Button onClick={submit} type="primary" size='large'> Submit </Button>
        </Row>

      </Content>

    </Layout>
    </>)}

export default Duty;
