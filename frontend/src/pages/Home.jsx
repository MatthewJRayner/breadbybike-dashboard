import React from 'react';
import HomeDashboard from '../dashboards/HomeDashboard';
import useRequireAccessLevel from '../components/requireAccessLevel';

const HomePage = () => {
  useRequireAccessLevel('manager');

  return (
    <HomeDashboard />
  );
};

export default HomePage;