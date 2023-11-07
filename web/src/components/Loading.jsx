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

const Loading = ({ size }) => (
  <RotatingLogo src={Logo} alt="Loading..." width={size} height={size} />
);

export default Loading;