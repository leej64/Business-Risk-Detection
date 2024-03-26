import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';
import newsData from './data/news_amzn_2018.json'

// Generate Order Data
function createData(id, date, title, ticker, link, risk_type) {
  return { id, date, title, ticker, link, risk_type };
}

const rows = [];

var cnt = 0;
for (var o in newsData) {
  if (newsData[o]["related_tickers"] !== "AMZN") continue;
  if (newsData[o]["publish_time"].substring(0, 10) >= "2018-07-01") continue;
  cnt += 1;
  rows.push(createData(
    cnt,
    newsData[o]["publish_time"],
    newsData[o]["title"],
    newsData[o]["related_tickers"],
    newsData[o]["link"],
    newsData[o]["risk_type"]
  ));
}

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
            <TableCell>Related Tickers</TableCell>
            <TableCell>Link</TableCell>
            <TableCell align="right">Risk Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id}>
              <TableCell>{row.date}</TableCell>
              <TableCell>{row.title}</TableCell>
              <TableCell>{row.ticker}</TableCell>
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
