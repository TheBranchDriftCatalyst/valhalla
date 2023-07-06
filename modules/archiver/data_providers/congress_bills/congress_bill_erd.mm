erDiagram
    CongressBill {
        string Congress
        string Number
        string OriginChamber
        string OriginChamberCode
        string Title
        string Type
        string UpdateDate
        string UpdateDateIncludingText
        string URL
    }

    LatestAction {
        string ActionDate
        string Text
    }

    CongressBill -- LatestAction : "has"