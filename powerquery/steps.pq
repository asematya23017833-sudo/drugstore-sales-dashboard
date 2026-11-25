// Power Query (M) load + model steps for the Power BI version
let
    Sales = Csv.Document(File.Contents("data\rossmann_train.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    SalesTyped = Table.TransformColumnTypes(Table.PromoteHeaders(Sales),
        {{"Store", Int64.Type}, {"Date", type date}, {"Sales", Int64.Type}, {"Customers", Int64.Type},
         {"Open", Int64.Type}, {"Promo", Int64.Type}, {"StateHoliday", type text}, {"SchoolHoliday", Int64.Type}}),
    OpenOnly = Table.SelectRows(SalesTyped, each [Open] = 1),
    Stores = Csv.Document(File.Contents("data\rossmann_store.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    StoresTyped = Table.TransformColumnTypes(Table.PromoteHeaders(Stores), {{"Store", Int64.Type}}),
    Merged = Table.NestedJoin(OpenOnly, {"Store"}, StoresTyped, {"Store"}, "StoreInfo", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "StoreInfo", {"StoreType", "Assortment"}, {"StoreType", "Assortment"})
in
    Expanded
