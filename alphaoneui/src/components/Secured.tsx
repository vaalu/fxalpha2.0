import { KEYCLOAK_JSON } from '../AppConstants'
import React, { Component } from 'react'
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/animate.min.css";
import "../assets/sass/light-bootstrap-dashboard-react.scss?v=1.3.0";
import "../assets/css/demo.css";
import "../assets/css/pe-icon-7-stroke.css";
import AdminLayout from "../layouts/Admin.jsx";

class Secured extends Component <{}, { keycloak:any, authenticated:boolean }> {

  constructor(props:any) {
    super(props)
    this.state = {
			keycloak:'', 
			authenticated: false
		}
  }

  componentDidMount() {
	  const keycloak = KEYCLOAK_JSON
	  keycloak.init({onLoad: 'login-required'}).success( (authenticated:any) => {
		  console.log('Authentication result: ', authenticated)
		  this.setState({
			  keycloak:keycloak, 
			  authenticated:authenticated
		  })
		  // this.setState({ keycloak: keycloak, authenticated: authenticated })
	  })
  }

  render() {
	  if (this.state.keycloak) {
		  console.log('Keycloak state', this.state)
		  const { keycloak } = this.state
		  if (this.state.authenticated) {
			  return (
				  <>
					<BrowserRouter>
						<Switch>
							<Route path="/admin" render={(props:any) => <AdminLayout {...props} keycloak={keycloak}/>} />
							<Redirect from="/" to={{pathname:'/admin/dashboard'}} />
						</Switch>
					</BrowserRouter>,
					document.getElementById("root")
				  </>
			  )
		  } else {
			  return (
				  <div>Unable to authenticate</div>
			  )
		  }
	  }
	  return (
		  <div>Keycloak initialization...</div>
	  )
  }
}
export default Secured;