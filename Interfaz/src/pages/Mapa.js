import React from 'react'
import { GoogleMap, useJsApiLoader } from '@react-google-maps/api';

const containerStyle = {
	position: "relative",
	width: '86vw',
    height: '89.5vh',
};

const center = {
	lat: 42.169771, 
	lng: -8.688262
};

const Mapa = () => {

	const { isLoaded } = useJsApiLoader({
		id: 'google-map-script',
		googleMapsApiKey: "AIzaSyAzS_9gyzOfj5YJoKcWvD3y-n-ZVbeQerI"
	})

	const [ map, setMap ] = React.useState(null)
	return isLoaded ? (
		<GoogleMap
		 mapContainerStyle={containerStyle}
		 center={center}
		 zoom={16}
		 mapTypeId='satellite'
		/>
	): <></>
}

export default Mapa;