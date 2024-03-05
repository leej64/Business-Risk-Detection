import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

export default function Company() {
  return (
    <React.Fragment>
      <Title>Company Info</Title>
      <Typography component="p" variant="h4">
        Nvidia
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on {new Date().getMonth() + 1}/{new Date().getDate()}/{new Date().getFullYear()}
      </Typography>
      <div>
        <Link color="primary" href="https://www.nvidia.com/en-us/">
          Company Website
        </Link>
      </div>
    </React.Fragment>
  );
}
