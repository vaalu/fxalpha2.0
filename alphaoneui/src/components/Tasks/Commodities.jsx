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
import Checkbox from "../CustomCheckbox/CustomCheckbox.jsx";
import CommoditiesData from '../../views/data/CommoditiesData'
import DashboardStore from '../../redux/store/DashboardStore'

export class Commodities extends Component {

  handleCheckbox = event => {
    const target = event.target;
    console.log(event.target);
    this.setState({
      [target.name]: target.checked,
      commodities: [],
      isConnected:[]
    });
  };

  async fetchCommodities() {
    await CommoditiesData().then(commodities => {
      commodities.forEach(item => (item.isChecked = true))
      this.setState({
        commodities : commodities
      })
    })
  }
  componentWillMount() {
    DashboardStore.subscribe(() => {
      this.setState({
        commodities : []
      })
      console.log('Refreshing scripts: ', DashboardStore.getState().refresh())
      if(DashboardStore.getState().refresh()) {
        this.fetchCommodities()
      }
    })
  }
  componentDidMount(){
    this.fetchCommodities()
  }
  render() {
    const tasks_title = this.state ? this.state.commodities ? this.state.commodities : [] : []
    var tasks = [];
    tasks.push(
      <tr>
        <td>Live</td>
        <td>Instrument</td>
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
          <td>{tasks_title[i].instrument}</td>
          <td className="td-actions text-right">{tasks_title[i].id}</td>
          <td className="td-actions text-right">{tasks_title[i].token}</td>
        </tr>
      );
    }
    return <tbody>{tasks}</tbody>;
  }
}

export default Commodities;
