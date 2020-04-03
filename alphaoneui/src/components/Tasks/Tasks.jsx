/*!

=========================================================
* Light Bootstrap Dashboard React - v1.3.0
=========================================================

* Product Page: https://www.creative-tim.com/product/light-bootstrap-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { Component } from "react";
import Checkbox from "components/CustomCheckbox/CustomCheckbox.jsx";
import ScripsData from '../../views/data/ScripsData'
import DashboardStore from '../../redux/store/DashboardStore'

export class Tasks extends Component {
  handleCheckbox = event => {
    const target = event.target;
    console.log(event.target);
    this.setState({
      [target.name]: target.checked,
      niftyScrips: [],
      isConnected:[]
    });
  };
  async fetchNifty() {
    await ScripsData().then(result => {
      console.log('ScripsData: ', result)
      result.scrips.forEach(item => (item.isChecked = true))
      this.setState({
        niftyScrips : result.scrips
      })
    })
    // console.log('Nifty 50 Stocks: ', this.state.niftyScrips.length)
  }
  componentWillMount() {
    DashboardStore.subscribe(() => {
      this.setState({
        niftyScrips : []
      })
      // console.log('Refreshing scripts: ', DashboardStore.getState().refresh())
      if(DashboardStore.getState().refresh()) {
        this.fetchNifty()
      }
    })
  }
  componentDidMount(){
    this.fetchNifty()
  }
  render() {
    const tasks_title = this.state ? this.state.niftyScrips ? this.state.niftyScrips : [] : []
    var tasks = [];
    tasks.push(
      <tr>
        <td>Live</td>
        <td>Company Name</td>
        <td className="td-actions text-right">Symbol</td>
        <td className="td-actions text-right">Instrument ID</td>
      </tr>
    )
    for (var i = 0; i < tasks_title.length; i++) {
      tasks.push(
        <tr key={i}>
          <td>
            <Checkbox number={tasks_title[i].zid} isChecked={tasks_title[i].isChecked} />
          </td>
          <td>{tasks_title[i].company}</td>
          <td className="td-actions text-right">{tasks_title[i].symbol}</td>
          <td className="td-actions text-right">{tasks_title[i].instrument_id}</td>
        </tr>
      );
    }
    return <tbody>{tasks}</tbody>;
  }
}

export default Tasks;
