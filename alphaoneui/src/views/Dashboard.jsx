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
import React, { Component } from "react"
import ChartistGraph from "react-chartist"
import { Grid, Row, Col } from "react-bootstrap"

import { Card } from "../components/Card/Card"
import { Commodities } from "../components/Tasks/Commodities"
import { StatsCard } from "../components/StatsCard/StatsCard"
import { Tasks } from "../components/Tasks/Tasks"

import DashboardStore from '../redux/store/DashboardStore'
import { DashboardActions } from '../redux/actions/DashboardActions'
import { DATE_CONSTANTS } from '../AppConstants'
import { FormInputs } from "../components/FormInputs/FormInputs.jsx"
import Button from "../components/CustomButton/CustomButton.jsx"
import WSDataConnect from "../views/data/WSDataConnect"

import {
  dataPie,
  legendPie,
  dataSales,
  optionsSales,
  responsiveSales,
  legendSales
} from "../variables/Variables.jsx";

class Dashboard extends Component {
  
  getFormattedDate() {
    const currDate = new Date()
    const day = currDate.getDate()
    const monthIndex = currDate.getMonth()
    const year = currDate.getFullYear()
    const hour = currDate.getHours()
    const minutes = currDate.getMinutes()
    const seconds = currDate.getSeconds()


    return day + '-' + DATE_CONSTANTS.months[monthIndex] + '-' + year + ' ' + hour + ':' + minutes + ':' + seconds
  }
  handleClick(event){
    event.preventDefault();
    const token = event.target.elements.aliceToken.value
    console.log("I am clicked from dashboard: ", token)
    WSDataConnect(token).then(result => {
      console.log("Fetched result from commodities: ", result)
    })
  }
  componentWillMount() {
    window.store = DashboardStore
    window.refreshAction = DashboardActions.statCardRefreshEquities()
    this.setState({
      stocksCount:50,
      updatedOn:this.getFormattedDate()
    })
    console.log('Store loaded? ', DashboardStore.getState())
    DashboardStore.subscribe(() => {
      console.log('Refreshed for count: ', DashboardStore.getState().refreshCount())
      this.setState({
        stocksCount : DashboardStore.getState().refreshCount(), 
        updatedOn:this.getFormattedDate()
      })
    })
  }
  
  createLegend(json) {
    var legend = [];
    for (var i = 0; i < json["names"].length; i++) {
      var type = "fa fa-circle text-" + json["types"][i];
      legend.push(<i className={type} key={i} />);
      legend.push(" ");
      legend.push(json["names"][i]);
    }
    return legend;
  }
  render() {
    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-wallet text-success" />}
                statsText="Total Stocks"
                statsValue={this.state.stocksCount}
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText={'Updated On ' + this.state.updatedOn } 
                isRefreshRequired={true}
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-cash text-success" />}
                statsText="Revenue"
                statsValue="[++]"
                statsIcon={<i className="fa fa-calendar-o" />}
                statsIconText="As of now"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-way text-danger" />}
                statsText="Errors"
                statsValue="23"
                statsIcon={<i className="fa fa-clock-o" />}
                statsIconText="In the last hour"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="fa fa-twitter text-info" />}
                statsText="Followers"
                statsValue="+45"
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText="Updated now"
              />
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Card
                title="Alice Token"
                category="Generate and publish alice ant token"
                stats="Updated 3 minutes ago"
                statsIcon="fa fa-history"
                content={
                  <div className="table-full-width">
                    <div style={{padding:'20px'}}>
                      <form onSubmit={(e) => this.handleClick(e)}>
                        <FormInputs
                            ncols={["col-md-12"]}
                            properties={[
                              {
                                label: "Alice Token",
                                type: "text",
                                bsClass: "form-control",
                                placeholder: "Alice Token", 
                                inputname:"aliceToken", 
                                name:'aliceToken', 
                                id:'aliceToken'
                              }
                            ]}
                        />
                        <Button bsStyle="info" pullRight fill type="submit" >
                          Connect
                        </Button>
                      </form>
                    </div>
                  </div>
                }
              />
            </Col>
          </Row>
          <Row>
           <Col md={6}>
              <Card
                title="Scripts"
                category="Connected for live updates"
                stats="Updated 3 minutes ago"
                statsIcon="fa fa-history"
                content={
                  <div className="table-full-width">
                    <table className="table">
                      <Tasks />
                    </table>
                  </div>
                }
              />
           </Col>
           <Col md={6}>
              <Card
                title="Commodities"
                category="Connected for live updates"
                stats="Updated 3 minutes ago"
                statsIcon="fa fa-history"
                content={
                  <div className="table-full-width">
                    <table className="table">
                      <Commodities />
                    </table>
                  </div>
                }
              />
           </Col>
          </Row>
          <Row>
            <Col md={8}>
              <Card
                statsIcon="fa fa-history"
                id="chartHours"
                title="Users Behavior"
                category="24 Hours performance"
                stats="Updated 3 minutes ago"
                content={
                  <div className="ct-chart">
                    <ChartistGraph
                      data={dataSales}
                      type="Line"
                      options={optionsSales}
                      responsiveOptions={responsiveSales}
                    />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendSales)}</div>
                }
              />
            </Col>
            <Col md={4}>
              <Card
                statsIcon="fa fa-clock-o"
                title="Email Statistics"
                category="Last Campaign Performance"
                stats="Campaign sent 2 days ago"
                content={
                  <div
                    id="chartPreferences"
                    className="ct-chart ct-perfect-fourth"
                  >
                    <ChartistGraph data={dataPie} type="Pie" />
                  </div>
                }
                legend={
                  <div className="legend">{this.createLegend(legendPie)}</div>
                }
              />
            </Col>
          </Row>

        </Grid>
      </div>
    );
  }
}

export default Dashboard;
