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
import { Row, Col } from "react-bootstrap";
import DashboardStore from '../../redux/store/DashboardStore'
import { DashboardActions } from '../../redux/actions/DashboardActions'

const handleClick = (evt) => {
  DashboardStore.dispatch(DashboardActions.statCardRefreshEquities(true))
}
const doINeedRefresh = (statsIcon, statsIconText, isRefreshRequired) => {
  if(isRefreshRequired) {
    return <div onClick={handleClick} >
        {statsIcon} <span style={{fontSize:'12px'}}>&nbsp;{statsIconText}</span>&nbsp;<i style={{cursor:'pointer'}} className="pe-7s-refresh-2 text-success" />
      </div>
  } else {
    return <div className="stats">
              {statsIcon} {statsIconText} 
            </div>
  }
}
export class StatsCard extends Component {
  render() {
    let content = doINeedRefresh(this.props.statsIcon, this.props.statsIconText, this.props.isRefreshRequired)
    return (
      <div className="card card-stats">
        <div className="content">
          <Row>
            <Col xs={5}>
              <div className="icon-big text-center icon-warning">
                {this.props.bigIcon}
              </div>
            </Col>
            <Col xs={7}>
              <div className="numbers">
                <p>{this.props.statsText}</p>
                {this.props.statsValue}
              </div>
            </Col>
          </Row>
          <div className="footer">
            <hr />
            {content}
          </div>
        </div>
      </div>
    );
  }
}

export default StatsCard;
