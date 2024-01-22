

def dialfire_sync_missing_orders_from_df(self):
        ref = self.dialfire_ref

        rjson = [
            {"values": ["lead_success"], "field": "$task"},
            {"values": ["2"], "field": "_limit_"}
        ]

        now = datetime.now()
        dt_from = self.dialfire_sync_dt or (now - timedelta(days=1))
        # Test: 2021-03-24t14:21:07.419z
        rjson.append({
            "values": [self.dialfire_date_time(dt_from)],
            "field": "$entry_date",
            "operator": "GT",
        })

        dt_to = datetime.now()
        # dt_to = dt_from + timedelta(days=1)
        # if dt_to > now:
        #     dt_to = now

        # rjson.append({
        #     "values": [self.dialfire_date_time(dt_to)],
        #     "field": "$entry_date",
        #     "operator": "LE",
        # })

        res = requests.request(
            method='POST',
            url=(
                f'https://api.dialfire.com/api/campaigns/{ref}'
                f'/contacts/filter'
            ),
            headers={
                'Authorization': f'Bearer {self.get_dialfire_token()}',
                'Content-Type': 'text/plain'
            },
            json=rjson,
        )

        if res.status_code != 200:
            raise exceptions.AccessError(
                f'Dialfire API: {res.content} for odoo campaign #{self.id}'
            )

        hits = json.loads(res.text)['hits']
        _logger.debug(f'Dialfire sync got {len(hits)} leads')
        for hit in hits:
            self._create_odoo_record(
                model='crm.lead',
                dialfire_id=hit['$id'],
            )
        self.dialfire_sync_dt = dt_to