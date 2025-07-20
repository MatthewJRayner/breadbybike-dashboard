import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const useRequireAccessLevel = (requiredLevel) => {
    const navigate = useNavigate();

    useEffect(() => {
        const userLevel = localStorage.getItem('accessLevel');
        if (!userLevel || (requiredLevel === 'manager' && userLevel !== 'manager')) {
            navigate('/login');
        }
    }, [requiredLevel, navigate]);
};

export default useRequireAccessLevel;