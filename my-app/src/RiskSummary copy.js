import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

export default function RiskSummary() {
  return (
    <React.Fragment>
      <Title>Risk Summary</Title>
      <Typography component="p" variant="h4">
        Low Risk
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on {new Date().getMonth() + 1}/{new Date().getDate()}/{new Date().getFullYear()}
      </Typography>
      <div>
        <Link color="primary" href="#">
          Detailed breakdown
        </Link>
      </div>
    </React.Fragment>
  );
}
