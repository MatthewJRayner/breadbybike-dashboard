import React from 'react';
import HomeDashboard from '../dashboards/HomeDashboard';
import useRequireAccessLevel from '../components/requireAccessLevel';

const HomePage = () => {
  useRequireAccessLevel('manager');
  if (localStorage.getItem('accessLevel') === 'manager') {
    return (
      <HomeDashboard />
    );
  } else {
    return (
      <div>You don't possess the required access.</div>
    );
  }
  
};

export default HomePage;