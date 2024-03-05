import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';

// Generate Order Data
function createData(id, date, title, author, link, risk_type) {
  return { id, date, title, author, link, risk_type };
}

const rows = [
  createData(
    0,
    '16 Mar, 2018',
    'AAA',
    'BBB',
    'yahoo',
    'None',
  )
];

function preventDefault(event) {
  event.preventDefault();
}

export default function News() {
  return (
    <React.Fragment>
      <Title>Recent News</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Title</TableCell>
            <TableCell>Author</TableCell>
            <TableCell>Link</TableCell>
            <TableCell align="right">Risk Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.date}</TableCell>
              <TableCell>{row.title}</TableCell>
              <TableCell>{row.author}</TableCell>
              <TableCell>{row.link}</TableCell>
              <TableCell align="right">{row.risk_type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 3 }}>
        See more news articles
      </Link>
    </React.Fragment>
  );
}
