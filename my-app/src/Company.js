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
        Amazon Inc.
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on 07/01/2018
      </Typography>
      <div>
        <Link color="primary" href="https://www.amazon.com/">
          Company Website
        </Link>
      </div>
    </React.Fragment>
  );
}
