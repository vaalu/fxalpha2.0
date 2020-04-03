import { REFRESH_STOCKS, REFRESH_STOCKS_COUNT } from '../ReduxConstants'
const initialState = {
	refresh: (objState:boolean) => {
				return objState
			}, 
	refreshCount: (objCount:number = 50) => {
				return objCount
			}
}
const dashboardReducer = (state = initialState, action:any) => {
	if (action.type === REFRESH_STOCKS) {
		return Object.assign({}, state, {
			refresh: () => {
				return state.refresh(action.payload)
			}
		})
	}
	if (action.type === REFRESH_STOCKS_COUNT) {
		return Object.assign({}, state, {
			refreshCount: () => {
				return state.refreshCount(action.payload)
			}
		})
	}
	return state
}
export default dashboardReducer