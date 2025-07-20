import React from 'react';
import ItemsDashboard from '../dashboards/ItemsDashboard'; 
import useRequireAccessLevel from '../components/requireAccessLevel';

const ItemsPage = () => {
    useRequireAccessLevel('manager');

    return (
        <ItemsDashboard />
    );
};

export default ItemsPage;