import React from 'react';
import { styled, keyframes } from '@mui/system';
import Logo from '../resources/siftbox_favicon.png';

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

const RotatingLogo = styled('img')({
    animation: `${rotate} 4s linear infinite`,
});

const Loading = () => (
    <RotatingLogo src={Logo} alt="Loading..." width="75" height="75" />
);

export default Loading;