import { createStore } from 'redux'
import DashboardReducer from '../reducers/DashboardReducer'

const DashboardStore = createStore(DashboardReducer)
export default DashboardStore